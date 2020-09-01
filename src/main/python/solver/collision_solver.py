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

    def __call__(self, body_info, contact_info):
        self.obj_num = len(body_info)
        return self.solve_integrate(body_info, contact_info)

    def solve_integrate(self, body_info, contact_info):
        pos, velocity, theta, omega, mass, inertia = self.extract_body_attr(body_info)
        contact, normal, manifold = self.extract_contact_attr(contact_info)
        generalized_velocity = self.get_generalized_velocity(velocity, omega)
        # pos, velocity, angular_v, mass, inertia, conn, manifold
        jacobian, bias, obj_idx=self.get_jacobian_with_bias(pos, velocity, omega, contact, normal, manifold)
        f_ext=self.get_external_force(mass)
        eta=bias/self.dt - self.sparse_dot_vec(jacobian, generalized_velocity/self.dt + self.get_inv_mass_dot_vec(mass, f_ext), obj_idx)
        force = self.PGS_solve(jacobian, mass, inertia, eta, obj_idx, self.solve_iters)
        generalized_velocity_next = generalized_velocity + self.dt*self.get_inv_mass_dot_vec(np.dot(jacobian.T, force)+f_ext)
        velocity_next, omega_next = self.retrieve_velocities_from_generalized(generalized_velocity_next)
        pos_next = pos[:,:2] + self.dt*velocity_next
        theta_next = theta + self.dt/2*omega_next*omega_next
        obj_attr = self.assemble_obj_attr(pos_next, theta_next, velocity_next, omega_next)
        return obj_attr

    def update_task(self, task_info, action_info):
        pass

    def get_generalized_velocity(self, velocity, omega):
        ret = []
        for i in range(self.obj_num):
            ret.append([velocity[i][0], velocity[i][1], 0.0, 0.0, 0.0, omega[i]])
        return np.concatenate(ret, axis=0)

    def vec_2d_to_3d(self, vec):
        return np.array([vec[0], vec[1], 0.0])

    def retrieve_velocities_from_generalized(self, generalized):
        velocity = []
        omega = []
        for i in range(self.obj_num):
            velocity.append(generalized[i][0:2])
            omega.append(generalized[i][5])
        velocity=np.array(velocity)
        omega=np.array(omega)
        return velocity, omega

    def get_external_force(self, mass):
        ret = []
        for i in range(self.obj_num):
            ret.append([0.0, -mass[i] * self.g, 0.0, 0.0, 0.0, 0.0])
        return np.concatenate(ret, axis=0)

    def extract_body_attr(self, body_info):
        pos = []
        velocity=[]
        theta=[]
        omega=[]
        mass=[]
        inertia=[]
        for id, info in enumerate(body_info['bodies']):
            pos.append(np.array([info['pos_x'], info['pos_y'], 0.0]))
            velocity.append(np.array([info['velocity_x'], info['velocity_y'], 0.0]))
            theta.append(info['angle'])
            omega.append(info['angular_velocity'])
            mass.append(info['mass'])
            inertia.append(info['inertia'])
        pos=np.stack(pos, axis=0)
        velocity=np.stack(velocity, axis=0)
        theta=np.stack(theta, axis=0)
        omega=np.stack(omega, axis=0)
        mass=np.stack(mass, axis=0)
        inertia=np.stack(inertia, axis=0)
        return pos, velocity, theta, omega, mass, inertia

    def extract_contact_attr(self, contact_info):
        contact=[]
        normal=[]
        manifold=[]
        if len(contact_info['contacts'])==0:
            contact = np.zeros([0,2])
            normal = np.zeros([0,3])
            manifold = np.zeros([0,3])
        else:
            for id, info in enumerate(contact_info['contacts']):
                contact.append(np.array(info['body_a'], info['body_b']))
                normal.append(self.vec_2d_to_3d(info['manifold_normal']))
                if info['point_count']==2:
                    manifold_2d=(info['points'][0]+info['points'][1])/2
                elif info['point_count']==1:
                    manifold_2d=info['points'][0]
                else:
                    raise RuntimeError()
                manifold.append(self.vec_2d_to_3d(manifold_2d))
            contact=np.stack(contact, axis=0)
            normal=np.stack(normal, axis=0)
            manifold=np.stack(manifold, axis=0)
        return contact, normal, manifold

    def assemble_obj_attr(self, pos_next, theta_next, velocity_next, omega_next):
        obj_attr = []
        for i in range(self.obj_num):
            obj_attr.append({'theta': theta_next[i], 'x': pos_next[i][0], 'y': pos_next[i][1],
                             'omega': omega_next[i], 'vx': velocity_next[i][0], 'vy': velocity_next[i][1]})
        return obj_attr

    def get_jacobian_with_bias(self, pos, velocity, omega, contact, normal, manifold):
        # jacobian: s x 12
        #
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
        if len(jacobian)==0:
            jacobian = np.zeros([0,12])
            obj_idx = np.zeros([0,2])
        else:
            jacobian=np.stack(jacobian, axis=0)
            obj_idx=np.stack(obj_idx, axis=0)
        bias=np.array(bias)
        return jacobian, bias, obj_idx

    def get_inv_mass_dot_vec(self, vec):
        for i in range(self.obj_num):
            vec[i*self.gv_channel, i*self.gv_channel+self.v_channel]/=vec[i]
        return vec

    def sparse_dot_vec(self, jacobian, vec, obj_idx):
        # J: s x 12
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
        if constraint_cnt==0:
            return np.zeros([0])
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