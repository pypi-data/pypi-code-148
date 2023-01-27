import cv2
import os
import numpy as np
import torch
from .util_recognition import compute_sim, compute_sims

def draw_result(img,faces,ga=False,race=False,to_bgr=False):
        dimg = img.copy()
        if to_bgr:
            dimg = cv2.cvtColor(dimg,cv2.COLOR_BGR2RGB)
        for i in range(len(faces)):
            face = faces[i]
            color = (0,255,0)
            x1,y1,x2,y2 = face.bbox.astype(np.int)
            
            cv2.rectangle(dimg,(x1,y1),(x2,y2),color,2)

            wtxt = ''
            if ga:
                if face.gender is not None and face.age is not None:
                    wtxt+="{} {}".format(face.gender, face.age)
                else:
                    wtxt+="{} {}".format('None','0')
            if race:
                if face.race is not None:
                    wtxt+=" {}".format(face.race)
                else:
                    wtxt+=" {}".format("None")

            if wtxt:
                cv2.putText(dimg, wtxt,(x1-1, y2+25),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)


        return dimg

def draw_result_land(img,faces,to_bgr=False,draw5=False,point_size=10):

        land_list = [ name for name in faces[0].keys() if "land" in name]

        dimg = img.copy()
        if to_bgr:
            dimg = cv2.cvtColor(dimg,cv2.COLOR_BGR2RGB)
        for i in range(len(faces)):
            face = faces[i]
            color = (0,255,0)
            if len(land_list)==1:
                lands = face[land_list[0]]
            elif not draw5:
                lands = face.land
            else:
                lands = face.land5
            for land in lands:
                x = int(land[0])
                y = int(land[1])
            
                cv2.line(dimg,(x,y),(x,y),color,point_size)

        return dimg

def draw_result_sim(img,faces,refs,sim_thresh=0.4,ga=True,to_bgr=False,max_sim=False,all_draw=False):
        dimg = img.copy()
        font_scale=1
        if to_bgr:
            dimg = cv2.cvtColor(dimg,cv2.COLOR_BGR2RGB)
        refs_keys = list(refs.keys())
        refs_feat = list(refs.values())
        
        for i in range(len(faces)):
            face = faces[i]
            
            # compute sim
            if max_sim:
                if face.max_flag:
                    sims = compute_sims(face.feat,refs_feat)
                    max_idx = np.argmax(sims)
                    if sims[max_idx]>sim_thresh:
                        sim_pname = refs_keys[max_idx]
                        color=(0,255,0)
                else:
                    if all_draw:
                        #sim_pname='unknown'
                        sim_pname=""
                        color=(255,0,0)
                    else:
                        continue
            else:
                sims = compute_sims(face.feat,refs_feat)
                max_idx = np.argmax(sims)
                if sims[max_idx]>sim_thresh:
                    sim_pname = refs_keys[max_idx]
                    color=(0,255,0)
                else:
                    if all_draw:
                        sim_pname=''
                        color=(255,0,0)
                    else:
                        continue
            
            x1,y1,x2,y2 = face.bbox.astype(np.int)
            
            cv2.rectangle(dimg,(x1,y1),(x2,y2),color,2)
            
            if ga:
                if face.gender is not None and face.age is not None:
                    cv2.putText(dimg, "{} {}".format(face.gender, face.age),(x1-1, y2+25),cv2.FONT_HERSHEY_SIMPLEX,font_scale,color,2)
                    if sim_pname:
                        cv2.putText(dimg, "{}".format(sim_pname),(x1-1, y2+45),cv2.FONT_HERSHEY_SIMPLEX,font_scale,color,2)
                else:
                    cv2.putText(dimg, "{} {}".format('None', '0'), (x1-1, y2+25),cv2.FONT_HERSHEY_SIMPLEX,font_scale,color,2)
                    if sim_pname:
                        cv2.putText(dimg, "{}".format(sim_pname), (x1-1, y2+45),cv2.FONT_HERSHEY_SIMPLEX,font_scale,color,2)
            else:
                if sim_pname:
                    cv2.putText(dimg,sim_pname,(x1-1, y2+25),cv2.FONT_HERSHEY_SIMPLEX,font_scale,color,2)
                

        return dimg

def torch2numpy(outs):
    if torch.is_tensor(outs):
        outs = np.array(outs)
    return outs  