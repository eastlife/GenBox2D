import numpy as np

class CollisionSolver():

    def __init__(self):
        self.dt=1.0/60
        self.g=10
        self.v_channel=3
        self.gv_channel=2*self.v_channel
        self.j_channel=2*self.gv_channel
        self.solve_iters=10
        self.restitution=0.3
        self.obj_num=None

    def update_task(self, task_info, action_info):
        pass

    def get_generalized_velocity(self, velocity, omega):
        ret = []
        for i in range(self.obj_num):
            ret.append([velocity[i][0], velocity[i][1], 0.0, 0.0, 0.0, omega[i]])
        return np.concatenate(ret, axis=0)

    def get_external_force(self, mass):
        ret = []
        for i in range(self.obj_num):
            ret.append([0.0, -mass[i] * self.g, 0.0, 0.0, 0.0, 0.0])
        return np.concatenate(ret, axis=0)

    def to_3d_vec(self, vec):
        return np.array([vec[0], vec[1], 0.0])


    def __call__(self, body_info, contact_info):
        pos, velocity, omega, mass, inertia = self.extract_body_attr(body_info)
        contact, normal, manifold = self.extract_contact_attr(contact_info)
        # pos, velocity, angular_v, mass, inertia, conn, manifold
        jacobian, bias, obj_idx=self.get_jacobian_with_bias(pos, velocity, omega, contact, normal, manifold)

        eta=bias/self.dt - self.sparse_dot_vec(jacobian, velocity/self.dt + self.get_inv_mass_dot_fext(mass), obj_idx)
        return self.PGS_solve(jacobian, mass, inertia, eta, obj_idx, self.solve_iters)

    def extract_body_attr(self, body_info):
        pos = []
        velocity=[]
        alpha=[]
        omega=[]
        mass=[]
        inertia=[]
        for id, info in enumerate(body_info['bodies']):
            pos.append(np.array([info['pos_x'], info['pos_y'], 0.0]))
            velocity.append(np.array([info['velocity_x'], info['velocity_y'], 0.0]))
            omega.append(np.array([0.0,0.0,info['angular_velocity']]))
            mass.append(info['mass'])
            inertia.append(info['inertia'])
        pos=np.stack(pos, axis=0)
        velocity=np.stack(velocity, axis=0)
        omega=np.stack(omega, axis=0)
        mass=np.stack(mass, axis=0)
        inertia=np.stack(inertia, axis=0)
        return pos, velocity, omega, mass, inertia

    def extract_contact_attr(self, contact_info):
        contact=[]
        normal=[]
        manifold=[]
        for id, info in enumerate(contact_info['contacts']):
            contact.append(np.array(info['body_a'], info['body_b']))
            normal.append(info['manifold_normal'])
            print('manifold special treatment needed')
            assert(0)
            manifold.append(info['points'][0])
        contact=np.stack(contact, axis=0)
        normal=np.stack(normal, axis=0)
        manifold=np.stack(manifold, axis=0)
        return contact, normal, manifold

    def get_jacobian_with_bias(self, pos, velocity, omega, contact, normal, manifold):

        jacobian = []
        obj_idx=[]
        bias=[]
        collision_cnt=contact.shape[0]
        for i in range(collision_cnt):
            # non-penatration:
            # normal points from objA to objB
            idx1, idx2 = contact[i][0], contact[i][1]
            constraint=[]
            constraint.append(normal[i])
            constraint.append(-np.cross(manifold[i]-pos[idx1], normal[i]))
            constraint.append(normal[i])
            constraint.append(np.cross(manifold[i]-pos[idx2], normal[i]))
            constraint=np.concatenate(constraint, axis=0)
            jacobian.append(constraint)
            obj_idx.append(np.array([idx1,idx2]))

            vn=np.dot(velocity[idx2]+np.cross(omega[idx2], manifold[i]-pos[idx2])-velocity[idx1]-np.cross(omega[idx1], manifold[i]-pos[idx1]))
            bias.append(self.restitution * vn)
        jacobian=np.stack(jacobian, axis=0)
        obj_idx=np.stack(obj_idx, axis=0)
        bias=np.array(bias)
        return jacobian, bias, obj_idx

    def get_inv_mass_dot_fext(self, mass):
        f_ext=self.get_external_force(mass)
        for i in range(self.obj_num):
            f_ext[i*self.gv_channel, i*self.gv_channel+self.v_channel]/=mass[i]
        return f_ext

    def sparse_dot_vec(self, jacobian, vec, obj_idx):
        # J: s x 6
        # vec: n x 3
        # ret: s
        s = jacobian.shape[0]
        ret = np.zeros(s)
        for i in range(s):
            idx1,idx2=obj_idx[i][0], obj_idx[i][1]
            ret[i]=np.dot(jacobian[i, :self.gv_channel], vec[idx1]) + np.dot(jacobian[i, self.gv_channel:], vec[idx2])
        return ret

    def gv_dot_inv_mass(self, gv, mass, inertia):
        gv[:self.v_channel] /= mass
        gv[self.v_channel:] /= inertia
        return gv

    def sparse_dot_inv_mass(self, jacobian, mass, inertia, obj_idx):
        s = jacobian.shape[0]
        B=jacobian.copy()
        for i in range(s):
            idx1,idx2=obj_idx[i][0], obj_idx[i][1]
            self.gv_dot_inv_mass(B[i][:self.gv_channel], mass[idx1], inertia[idx1])
            self.gv_dot_inv_mass(B[i][self.gv_channel:], mass[idx2], inertia[idx2])
        return B

    def scatter_dot(self, matrix, vec, obj_idx):
        # mat: s x 6
        # vec: s
        # ret: n x 3
        s = matrix.shape[0]
        ret=np.zeros(s)
        for i in range(s):
            ret[obj_idx[0]]+=matrix[i][:self.gv_channel] * vec[i]
            ret[obj_idx[1]]+=matrix[i][self.gv_channel:] * vec[i]
        pass

    def get_initial_force(self):
        print('force caching not implemented')
        assert(0)
        pass

    def PGS_solve(self, jacobian, mass, inertia, eta, obj_idx, niter=10):
        # jacobian: s x 6
        # inv_mass: n x 3
        # eta: s
        # obj_idx: s x 2
        constraint_cnt=jacobian.shape[0]
        force=self.get_initial_force()
        B_T=self.sparse_dot_inv_mass(jacobian, mass, inertia, obj_idx)
        # B_T: s x 6
        a=self.scatter_dot(B_T, force, obj_idx)
        # a: n x 3
        d=np.zeros([constraint_cnt])
        for i in range(constraint_cnt):
            d[i]=np.dot(jacobian[i], B_T[i])
        for iter in range(niter):
            for i in constraint_cnt:
                b1,b2=obj_idx[i]
                dforce_i=eta[i]-np.dot(jacobian[i,:self.v_channel], a[b1])-np.dot(jacobian[i,self.v_channel:], a[b2])
                force_i_0=force[i]
                force_i=max(0, force_i_0 + dforce_i)
                dforce_i=force_i-force_i_0
                a[b1]+=dforce_i*B_T[i, :self.v_channel]
                a[b2]+=dforce_i*B_T[i, self.v_channel:]
        return force
