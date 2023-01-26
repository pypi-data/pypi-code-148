import os
import numpy as np

from ..model.load_arcface import Arcface


class FaceDB:
    def __init__(self):
        self.db={}
        self.db_size=0
        self.emd_size=512
        self.update_flag=False

    def add(self, idname, feat):
        if feat.shape==(512,): # feat shape = (1,512)
            feat = np.expand_dims(feat,axis=0)

        if idname in self.db:
            feat = feat / np.linalg.norm(feat)
            self.update(idname,feat)
        else:
            feat = feat / np.linalg.norm(feat)
            self.db[idname]=feat
            self.update_flag=True
            self.db_size+=1

    def get(self,idname):
        return self.db[idname]
                
    def update(self, idname, feat): 
        if not idname in self.db:
            self.add(idname,feat)
        else:
            self.db[idname]=feat
            self.update_flag=True

    def delete(self, idname):
        if idname in self.db:
            del self.db[idname]
            self.db_size-=1
            self.update_flag=True


class FaceRecog:
    def __init__(self,db_obj):

        self.available_models=[
            'glint360k-r50-arcface_multiple','glint360k-r100-arcface_multiple','glint360k-r100m-arcface_multiple', \
            'glint360k-r100m-pfc-arcface_multiple','glint360k-r200-arcface_multiple','glint360k-r200-pfc-arcface_multiple', \
            'glint360k-r200m-pfc-arcface_multiple','ms1m-r50m-arcface_multiple','ms1m-r100m-arcface_multiple']


        self.available_types=[
            'onnx','openvino'
        ]

        self.init_db(db_obj)

    def init_db(self,db_obj):
        self.db_features = np.array(list(db_obj.db.values()))
        self.db_ids = np.array(list(db_obj.db.keys()))
        db_obj.update_flag=False

    def check_update(self,db_obj):
        
        if db_obj.update_flag:
            self.db_features = np.array(list(db_obj.db.values()))
            self.db_ids = np.array(list(db_obj.db.keys()))
            db_obj.update_flag=False

    # feature
    # model type ( onnx v8.trt openvino )
    def load_model(self,model_type,model_path,device='cuda'):
            
        if model_type=='openvino':
            model_format='xml'
        else:
            model_format = model_type

        model_path = model_path+".{}".format(model_format)
        model = Arcface(model_type, model_path,onnx_device=device)
        self.model = model

        print("Load model: {}".format(model_path))
        print("Get Feature -> self.get_feature(img) !")

    def get_feature(self,img): # get_feature 시, normalization 된 feature 가 return
        if self.model is None:
            print("Model is None, Need load model (self.load_model(model_type,model_path,device='cuda'))")
            return None
        feat = self.model.get(img)
        feat = feat / np.linalg.norm(feat)

        return feat


    # 0~2 의 값 ( 0 타인 / 2 본인 )
    def match_score(self,db_obj,feat_src,score_th=1.0,topk=None): # db, feat_src 모두 normalization 된 feat 기준
        
        self.check_update(db_obj)

        if feat_src.shape==(512,): # feat shape = (1,512)
            feat_src = np.expand_dims(feat_src,axis=0)

        scores_ = np.sum(feat_src*self.db_features,-1)
        scores_new = np.array([1+(max(-1,min(1,v))) for v in scores_])

        # score th 
        if score_th is None:
            scores = scores_new
            ids = self.db_ids
        else:
            filter_idx = np.where(scores_new>=score_th)[0]
            scores = scores_new[filter_idx]
            ids = self.db_ids[filter_idx]
            
        if topk is None or topk>db_obj.db_size:
            topk = db_obj.db_size
            
        max_sort = np.argsort(scores,axis=0)
            
        top_ids = ids[max_sort[:topk]]
        top_scores = scores[max_sort[:topk]]
            
        return top_ids, top_scores

    def match_face_11_feature(self,feat1,feat2): # norm feat : norm feat

        if feat1.shape==(512,): # feat shape = (1,512)
            feat1 = np.expand_dims(feat1,axis=0)

        if feat2.shape==(512,): # feat shape = (1,512)
            feat2 = np.expand_dims(feat2,axis=0)

        scores_ = np.sum(feat1*feat2,-1)
        scores_new = np.array([1+(max(-1,min(1,v))) for v in scores_])

        return scores_new[0]

    def match_face_11_image(self,aligned1, aligned2): # aligned image : aligned image
        feat1 = self.get_feature(aligned1)
        feat2 = self.get_feature(aligned2)

        scores_ = np.sum(feat1*feat2,-1)
        scores_new = np.array([1+(max(-1,min(1,v))) for v in scores_])
            
        return scores_new[0]

    def match_face_1n_image(self,db_obj,aligned_src,score_th=1.0, topk=None): # aligned image : db

        feat_src = self.get_feature(aligned_src)
        return self.match_score(db_obj,feat_src,score_th=score_th, topk=topk)

    def match_face_1n_feature(self,db_obj,feat_src,score_th=1.0, topk=None): # norm feat : db

        return self.match_score(db_obj,feat_src,score_th=score_th, topk=topk)

    
