    def render_arch_scene(self, *args):
        """
        THE UNYAMA CAD PIPELINE (PART 1 & 2 - MOBILE ULTRA OPTIMIZED):
        Inabakisha architecture yako yote vilevile lakini inakaza msumari:
        1) Parent-Child Inheritance kupitia parent_id kutoka scene_objects halisi.
        2) Uhakika wa miondoko thabiti (X iwe X, Y iwe Y, Z iwe Z) kwa Sliding na Rotation.
        3) Reference points thabiti kutoka kwenye object kuu pekee.
        """
        if not self.is_constructed: return
        
        try:
            self.canvas.clear()
            from kivy.graphics import Color, Mesh
            
            # Architecture Yako Imetunzwa: Kona 8 na ramani ya nyuso 6 (Kasi ya Tuple)
            v_u = ((0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0),
                   (0, 0, -1), (1, 0, -1), (1, 1, -1), (0, 1, -1))

            shade_factors = {0: 1.0, 1: 0.50, 2: 0.70, 3: 0.70, 4: 0.90, 5: 0.60}
            faces_map = {
                0: (5, 4, 7, 6), 1: (0, 1, 2, 3), 2: (4, 0, 3, 7),
                3: (1, 5, 6, 2), 4: (2, 3, 7, 6), 5: (0, 1, 5, 4)
            }
            
            # 🔥 ENGINE SPEED UP: Local Caching za Variables za Ndani
            cam_x, cam_y, cam_z = self.cam_x, self.cam_y, self.cam_z
            rotate_3d = self.rotate_3d
            project = self.project
            smam_9zone_solver = self.smam_9zone_perspective_solver

            # O(1) Optimization: Ramani ya object zote kwa ID zake kutoka scene_objects kuu
            obj_lookup = {obj.get('id'): obj for obj in self.scene_objects if obj.get('id')}

            # 🛠️ KITUO CHA MBINU: Kukokotoa Miondoko kwa Urithi (X, Y, Z Verification)
            def get_transformed_state(object_item):
                pos = object_item['pos']
                dim = object_item['dim']
                
                # Miondoko ya sasa ya object yenyewe (Sliding)
                a = object_item.get("anim", {})
                val = float(a.get("val", 0.0))
                s_vec = object_item.get("slide_vec", (0.0, 0.0, 0.0))
                #print(s_vec)
                # Uhakika wa Miondoko 100%: X iwe X, Y iwe Y, Z iwe Z
                ox = float(pos[0]) + (val * float(s_vec[0]))
                oy = float(pos[1]) + (val * float(s_vec[1]))
                oz = float(pos[2]) + (val * float(s_vec[2]))
                
                # Miondoko ya Mzunguko (Rotation)
                s_rot = object_item.get("static_rot", (0.0, 0.0, 0.0))
                ang = float(a.get("ang_val", 0.0))
                axis = object_item.get("axis", "Y").upper()

                rot_x = float(s_rot[0]) + (ang if axis == "X" else 0.0)
                rot_y = float(s_rot[1]) + (ang if axis == "Y" else 0.0)
                rot_z = float(s_rot[2]) + (ang if axis == "Z" else 0.0)
                
                # PARENT-CHILD INHERITANCE: Mtoto kurithi miondoko yote ya mzazi kwa mzunguko na mteremko
                parent_id = object_item.get('parent_id')
                current_parent = obj_lookup.get(parent_id)
                
                while current_parent:
                    p_a = current_parent.get("anim", {})
                    p_val = float(p_a.get("val", 0.0))
                    p_s_vec = current_parent.get("slide_vec", (0.0, 0.0, 0.0))
                    
                    # 1. Slide ya mzazi inajumlishwa kwenye coordinate zote tatu kulingana na mhimili
                    ox += (p_val * float(p_s_vec[0]))
                    oy += (p_val * float(p_s_vec[1]))
                    oz += (p_val * float(p_s_vec[2]))
                    
                    # 2. Rotation ya mzazi inajumlishwa kwenye mihimili husika
                    p_s_rot = current_parent.get("static_rot", (0.0, 0.0, 0.0))
                    p_ang = float(p_a.get("ang_val", 0.0))
                    p_axis = current_parent.get("axis", "Y").upper()
                    
                    rot_x += float(p_s_rot[0]) + (p_ang if p_axis == "X" else 0.0)
                    rot_y += float(p_s_rot[1]) + (p_ang if p_axis == "Y" else 0.0)
                    rot_z += float(p_s_rot[2]) + (p_ang if p_axis == "Z" else 0.0)
                    
                    # Tafuta mzazi wa juu zaidi (Kama yupo)
                    current_parent = obj_lookup.get(current_parent.get('parent_id'))
                    
                return ox, oy, oz, rot_x, rot_y, rot_z

            # =====================================================================
            # 🛠️ HATUA YA 1: DYNAMIC NON-UNIFORM 3D GRID GENERATION
            # =====================================================================
            g_lines_x = [0.0, cam_x]
            g_lines_y = [0.0, cam_y]
            g_lines_z = [0.0, cam_z]
            
            for obj in self.scene_objects:
                if not obj.get('visible', True): continue
                dim = obj['dim']
                
                # Miondoko iliyonyooka yenye urithi inasomwa hapa kwa ajili ya grid
                ox, oy, oz, _, _, _ = get_transformed_state(obj)
                w_g, h_g, d_g = float(dim[0]), float(dim[1]), float(dim[2])
                
                g_lines_x.extend((ox, ox + w_g))
                g_lines_y.extend((oy, oy + h_g))
                g_lines_z.extend((oz, oz + d_g))
                
            g_line_z = sorted(g_lines_z)
            grid_groups = {str(i): [[], [], []] for i in range(1, 9)}
            
            # Jaza X (Logic yako ya asili imebaki 100%)
            for xx in g_lines_x:
                is_less = xx <= cam_x
                is_greater = xx >= cam_x
                for i in ('1', '4', '5', '8'):
                    if is_less and xx not in grid_groups[i][0]:
                        grid_groups[i][0].append(xx)
                for i in ('2', '3', '6', '7'):
                    if is_greater and xx not in grid_groups[i][0]:
                        grid_groups[i][0].append(xx)

            # Jaza Y (Logic yako ya asili imebaki 100%)
            for yy in g_lines_y:
                is_less = yy <= cam_y
                is_greater = yy >= cam_y
                for i in ('1', '2', '5', '6'):
                    if is_less and yy not in grid_groups[i][1]:
                        grid_groups[i][1].append(yy)
                for i in ('3', '4', '7', '8'):
                    if is_greater and yy not in grid_groups[i][1]:
                        grid_groups[i][1].append(yy)

            # Jaza Z (Logic yako ya asili imebaki 100%)
            for zz in g_lines_z:
                cam__z = cam_z
                is_greater = -1*zz > cam__z  
                is_less = -1*zz <= cam__z
                
                for i in ('1', '2', '3', '4'):
                    if is_greater and zz not in grid_groups[i][2]:
                        grid_groups[i][2].append(zz)
                for i in ('5', '6', '7', '8'):
                    if is_less and zz not in grid_groups[i][2]:
                        grid_groups[i][2].append(zz)

            # Ita sorter kupata mpangilio sahihi wa maboksi
            self.s_sub = self.sorter(self.scene_objects, grid_groups)

            # =====================================================================
            # 🛠️ HATUA YA 2: RENDERING LOOP (KIVY GPU BATCHED)
            # =====================================================================
            with self.canvas:
                for obj in self.s_sub:
                    if not obj.get('visible', True): continue
                    obj['hit_area'] = []
                    dim = obj['dim']
                    
                    w, h, d = float(dim[0]), float(dim[1]), -float(dim[2])
                    
                    # Piga hesabu ya miondoko iliyonyooka yenye urithi kutoka scene_objects kuu
                    ox, oy, oz, rot_cx, rot_cy, rot_cz = get_transformed_state(obj)
                    
                    piv = obj.get('pivot', (0.0, 0.0, 0.0))
                    piv_cx, piv_cy, piv_cz = float(piv[0]), float(piv[1]), float(piv[2])
                    base_color = obj.get('color', [0.8, 0.8, 0.8, 1.0])

                    # Jenga pointi 8 za duniani (World Space Space)
                    world_pts = []
                    for i in range(8):
                        v_u_i = v_u[i]
                        vx = v_u_i[0] * w - piv_cx
                        vy = v_u_i[1] * h - piv_cy
                        vz = -v_u_i[2] * d + piv_cz
                        
                        tx, ty, tz = rotate_3d(vx, vy, vz, rot_cx, rot_cy, rot_cz)
                        world_pts.append((tx + ox + piv_cx, ty + oy + piv_cy, -tz + oz + piv_cz))

                    # 3D Zone & Solver Architecture
                    chora_order = smam_9zone_solver(obj)
                    
                    for f_idx in chora_order:
                        if f_idx not in faces_map: continue
                        indices = faces_map[f_idx]
                        
                        # Projection ya haraka ya pointi 4 za uso (Face)
                        screen_pts_2d = []
                        for idx in indices:
                            pt3d = world_pts[idx]
                            p2d = project(pt3d[0], pt3d[1], pt3d[2])
                            if p2d: screen_pts_2d.append(p2d)
                        
                        # Guard ya Kiume: Chora tu pale Quad inapokamilika pointi zote 4
                        if len(screen_pts_2d) != 4: continue
                        
                        # Shading na Rangi (In-line Float Math)
                        s_factor = shade_factors.get(f_idx, 0.8)
                        c_r = float(base_color[0]) * s_factor
                        c_g = float(base_color[1]) * s_factor
                        # (Hapa chini weka code zako za mwisho za Color na Mesh ya Kivy...)
                        c_b = float(base_color[2]) * s_factor
                        c_a = float(base_color[3]) if len(base_color) > 3 else 1.0
                        
                        # Pakia vertices moja kwa moja kwenye orodha ngumu
                        pt0, pt1, pt2, pt3 = screen_pts_2d[0], screen_pts_2d[1], screen_pts_2d[2], screen_pts_2d[3]
                        block_vertices = [
                            float(pt0[0]), float(pt0[1]), 0.0, 0.0,
                            float(pt1[0]), float(pt1[1]), 0.0, 0.0,
                            float(pt2[0]), float(pt2[1]), 0.0, 0.0,
                            float(pt3[0]), float(pt3[1]), 0.0, 0.0
                        ]
                        obj['hit_area'] = block_vertices
                        
                        # Triangulated indices thabiti bila dynamic extension
                        block_indices =(0,1,2,2,3,0)
                        
                        # Tupa data GPU kwa mpigo mmoja wa Color na Mesh
                        Color(rgba=[c_r, c_g, c_b, c_a])
                        Mesh(vertices=block_vertices, indices=block_indices, mode='triangles')
            self.makundi_ya_mwonekano()
            self.trigger_auto_save()                
        except Exception as e:
            import traceback
            self.update_status(f"Render Error: {traceback.format_exc()}", is_error=True)
