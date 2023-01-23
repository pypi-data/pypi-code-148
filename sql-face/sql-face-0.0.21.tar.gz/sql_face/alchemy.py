# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/02_alchemy.ipynb.

# %% auto 0
__all__ = ['get_session', 'create_detectors', 'create_embedding_models', 'create_quality_models', 'fill_cropped_image_serfiq',
           'fill_cropped_image_general', 'create_cropped_images', 'create_face_images', 'create_quality_images',
           'update_gender', 'update_age', 'update_emotion', 'update_race', 'update_images', 'update_cropped_images',
           'update_face_images', 'update_embeddings_deepface', 'update_embeddings_qmagface', 'update_quality_images',
           'update_ser_fiq', 'update_tface']

# %% ../nbs/02_alchemy.ipynb 4
import os

from typing import List
from tqdm import tqdm

from sqlalchemy import create_engine, or_
from sqlalchemy.orm import sessionmaker

from deepface.commons import functions
from deepface import DeepFace

from sql_face.databases import FaceDataBase
from sql_face.tables import Base, Image, Detector, CroppedImage, EmbeddingModel, FaceImage, QualityModel, QualityImage 
from sql_face.tables import Gender, Age, Race, Emotion
from sql_face.tface import get_network, compute_tf_quality
from sql_face.qmagface import load_model, compute_qmagface_embeddings

# %% ../nbs/02_alchemy.ipynb 6
def get_session(
    output_dir:str, # Output directory
    db_name:str, # .db file name
                    ): # SQL alchemy session 
    db_path = os.path.join(output_dir,db_name+'.db')       
    engine = create_engine(f"sqlite:///{db_path}")
    if not os.path.exists(db_path):
        if not os.path.exists(output_dir):
            print(f'Creating output directory at {output_dir}')
            os.mkdir(output_dir)
            
        print(f'Creating Db file at {db_path}')        
    
    # If the database file exists, update the tables in Base
    Base.metadata.create_all(engine, checkfirst=True)
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    return session

# %% ../nbs/02_alchemy.ipynb 8
def create_detectors(session, #SQL alchemy session object
                    detector_names: List[str] # List of detectors to add to the database.
                    ):
    existing_detectors = {d.name for d in session.query(Detector).all()}
    new_detectors = [Detector(name=name) for name in detector_names if name not in existing_detectors]
    session.bulk_save_objects(new_detectors)
    session.commit()

# %% ../nbs/02_alchemy.ipynb 10
def create_embedding_models(session, #SQL alchemy session object
                            embedding_model_names: List[str]): # List of detectors to add to the database.
    existing_models = {em.name for em in session.query(EmbeddingModel).all()}
    new_models = [EmbeddingModel(name=name) for name in embedding_model_names if name not in existing_models]
    session.bulk_save_objects(new_models)
    session.commit()

# %% ../nbs/02_alchemy.ipynb 12
def create_quality_models(session, #SQL alchemy session object
                        quality_model_names: List[str]): # List of quality models to add to the database.
    existing_models = {qm.name for qm in session.query(QualityModel).all()}
    new_models = [QualityModel(name=name) for name in quality_model_names if name not in existing_models]
    session.bulk_save_objects(new_models)
    session.commit()

# %% ../nbs/02_alchemy.ipynb 14
def fill_cropped_image_serfiq(cr_img: CroppedImage, # CroppedImage object to be filled with bounding box and landmarks information.
                                input_dir, # Directory where the images are stored.
                                ser_fiq): #SERFIQ model object.
                                
        image = cr_img.images.get_image(input_dir)
        aligned_img = ser_fiq.apply_mtcnn(image)
        if aligned_img is None:
            cr_img.bounding_box = []
            cr_img.landmarks = []
            cr_img.face_detected = False
        elif len(aligned_img) == 0:
            cr_img.bounding_box = []
            cr_img.landmarks = []
            cr_img.face_detected = False
        else:
            bbox, points = ser_fiq.detector.detect_face(image)
            cr_img.bounding_box = bbox[0].tolist()
            cr_img.landmarks = points[0].tolist()
            cr_img.face_detected = True

# %% ../nbs/02_alchemy.ipynb 15
def fill_cropped_image_general(cr_img: CroppedImage, input_dir, **kwargs):
    image = cr_img.images.get_image(input_dir)      
    
    try:
        img_cropped, bounding_box = functions.preprocess_face(img=image,
                                                                detector_backend=cr_img.detectors.name,
                                                                enforce_detection=True,
                                                                return_region=True)
        
        cr_img.bounding_box = bounding_box
        cr_img.face_detected = True

    except ValueError:
        cr_img.bounding_box = []
        cr_img.face_detected = False
        #todo: change warning if the image is a video(frame).
        print(f'Face not found in {cr_img.images.path} with {cr_img.detectors.name}')



# %% ../nbs/02_alchemy.ipynb 16
def create_cropped_images(session, input_dir:str, serfiq = None):
        
        all_detectors = (session.query(Detector).all())
        for det in all_detectors:

            # Load SERFIQ model if neccesary
            if det.name == 'mtcnn_serfiq':
                
                fill_cropped_image = fill_cropped_image_serfiq
            else:
                
                fill_cropped_image = fill_cropped_image_general

            subquery = session.query(CroppedImage.image_id) \
                .filter(CroppedImage.detectors == det)
            images = (
                session.query(Image)
                    .filter(Image.image_id.notin_(subquery))
                    .all()
            )

            cropped_images = []
            count = 0
            for img in tqdm(images, desc=f'Creating CroppedImages for detector {det.name}'):
               
                cropped_image = CroppedImage()
                cropped_image.image_id = img.image_id
                cropped_image.detector_id = det.detector_id
                cropped_image.images = img
                cropped_image.detectors = det
                fill_cropped_image(cropped_image, input_dir, ser_fiq = serfiq)
                cropped_images.append(cropped_image)
                count += 1


                if count % 100 == 0:
                    session.bulk_save_objects(cropped_images)
                    try:
                        session.commit()
                    except IntegrityError:
                        session.rollback()
                        raise IntegrityError("Could not commit CroppedImages")
                    cropped_images = []
                    

            if cropped_images:          
                session.bulk_save_objects(cropped_images)
                try:
                    session.commit()
                except IntegrityError:
                    session.rollback()
                    raise IntegrityError("Could not commit CroppedImages")

# %% ../nbs/02_alchemy.ipynb 18
def create_face_images(session):
    all_embedding_models = (session.query(EmbeddingModel).all())
    for emb in tqdm(all_embedding_models, desc='Embedding models'):
        subquery = session.query(FaceImage.croppedImage_id) \
            .filter(FaceImage.embeddingModels == emb)
        cropped_images = (
            session.query(CroppedImage) \
                .filter(CroppedImage.croppedImage_id.notin_(subquery),
                        CroppedImage.face_detected == True)
                .all()
        )
        count = 0
        face_images_to_add = []
        for cr_img in tqdm(cropped_images, desc=f'Face images in {emb.name}'):
            face_image = FaceImage(croppedImage_id=cr_img.croppedImage_id, embeddingModel_id=emb.embeddingModel_id)
            face_images_to_add.append(face_image)
            count += 1
            if count % 100 == 0:
                session.bulk_save_objects(face_images_to_add)
                session.commit()
                face_images_to_add = []

            if count % 100 == 0:
                session.bulk_save_objects(face_images_to_add)
                try:
                    session.commit()
                except IntegrityError:
                    session.rollback()
                    raise IntegrityError("Could not commit face images")
                face_images_to_add = []

        if face_images_to_add:
            session.bulk_save_objects(face_images_to_add)
            try:
                session.commit()
            except IntegrityError:
                session.rollback()
                raise IntegrityError("Could not commit face images")

# %% ../nbs/02_alchemy.ipynb 20
def create_quality_images(session):
    all_quality_models = (session.query(QualityModel).all())
    
    for qua in tqdm(all_quality_models, desc='Quality models'):
        subquery = session.query(QualityImage.faceImage_id) \
            .filter(QualityImage.qualityModels == qua)
        face_images = (
            session.query(FaceImage) \
                .filter(FaceImage.faceImage_id.notin_(subquery))
                .all()
        )

        count = 0
        qua_images = []

        for face_img in tqdm(face_images, desc=f'Quality images in {qua.name}'):
            qua_image = QualityImage()
            qua_image.faceImages = face_img
            qua_image.qualityModels = qua
            qua_image.faceImage_id = face_img.faceImage_id
            qua_image.qualityModel_id = qua.qualityModel_id
            qua_images.append(qua_image)
            count += 1


            if count % 100 == 0:
                session.bulk_save_objects(qua_images)
                try:
                    session.commit()
                except IntegrityError:
                    session.rollback()
                    raise IntegrityError("Could not commit quality images")
                qua_images = []


    if qua_images:
        session.bulk_save_objects(qua_images)
        try:
            session.commit()
        except IntegrityError:
            session.rollback()
            raise IntegrityError("Could not commit quality images")

# %% ../nbs/02_alchemy.ipynb 23
def update_gender(session, input_dir:str, databases:List[FaceDataBase], force_update: bool = False):

    for db in databases:
        query = session.query(Image).filter(Image.source == db.source)
        if not force_update:
            query = query.filter(Image.gender == None)
        all_img = (query.all())

        updated_images = []
        count = 0

        # for img in tqdm(all_img[:10], desc='TRIM Update gender'):
        for img in tqdm(all_img, desc='Update gender'):

            try:
                filters = DeepFace.analyze(img_path=img.get_image(input_dir), actions=['gender'], enforce_detection=True, detector_backend = 'mediapipe') # detector_backend = 'mediapipe'
                img.gender = Gender(filters["gender"])
                
            except ValueError:
                img.gender = None

            updated_images.append({"image_id": img.image_id, "gender": img.gender})
            
            count += 1
            if count % 100 == 0:
                session.bulk_update_mappings(Image, updated_images)
                session.commit()
                updated_images = []
        if updated_images:
            session.bulk_update_mappings(Image, updated_images)
            session.flush()
        session.commit()

# %% ../nbs/02_alchemy.ipynb 25
def update_age(session, input_dir:str, databases:List[FaceDataBase],force_update: bool = False):
    for db in databases:
        query = session.query(Image).filter(Image.source == db.source)
        if not force_update:
            query = query.filter(Image.age == None)
        all_img = (query.all())

        updated_images = []
        count = 0

        for img in tqdm(all_img, desc='Update age'):
            try:
                filters = DeepFace.analyze(img_path=img.get_image(input_dir), actions=['age'], enforce_detection=True, detector_backend = 'mediapipe')
                age = filters["age"]
                img.age_number = age
                img.age = Age.age2enum(age)

                
            except ValueError:
                img.age = None
                img.age_number = None
                
                

            updated_images.append({"image_id": img.image_id, "age_number": img.age_number, "age": img.age})
            
            count += 1

            if count % 100 == 0:
                session.bulk_update_mappings(Image, updated_images)
                session.flush()
                session.commit()
                updated_images = []

        if updated_images:
            session.bulk_update_mappings(Image, updated_images)
            session.flush()
        session.commit()



# %% ../nbs/02_alchemy.ipynb 27
def update_emotion(session, input_dir:str, databases:List[FaceDataBase],force_update: bool = False):

    for db in databases:
        query = session.query(Image).filter(Image.source == db.source)
        if not force_update:
            query = query.filter(Image.emotion == None)
        all_img = (query.all())

        updated_images = []
        count = 0

        for img in tqdm(all_img, desc='Update facial expression (emotion)'):

            try:
                filters = DeepFace.analyze(img_path=img.get_image(input_dir), actions=['emotion'], enforce_detection=True, detector_backend = 'mediapipe')
                emotions = filters["emotion"]
                prime_emotion = max(emotions, key=emotions.get)
                img.emotion = Emotion(prime_emotion)
            except ValueError:
                img.emotion = None

            updated_images.append({"image_id": img.image_id, "emotion": img.emotion})
            
            count += 1
            if count % 100 == 0:
                session.bulk_update_mappings(Image, updated_images)
                session.flush()
                session.commit()
                updated_images = []
        if updated_images:
            session.bulk_update_mappings(Image, updated_images)
            session.flush()
        session.commit()


# %% ../nbs/02_alchemy.ipynb 29
def update_race(session, input_dir:str, databases:List[FaceDataBase], force_update: bool = False):
    
    for db in databases:
        query = session.query(Image).filter(Image.source == db.source)
        if not force_update:
            query = query.filter(Image.race == None)
        all_img = (query.all())

        updated_images = []
        count = 0

        for img in tqdm(all_img, desc='Update race'):
            try:
                filters = DeepFace.analyze(img_path=img.get_image(input_dir), actions=['race'], enforce_detection=True, detector_backend = 'mediapipe')
                races = filters["race"]
                prime_race = max(races, key=races.get)
                img.race = Race(prime_race)
            except ValueError:
                img.race = None

            updated_images.append({"image_id": img.image_id, "race": img.race})
            count += 1
            if count % 100 == 0:
                session.bulk_update_mappings(Image, updated_images)
                session.flush()
                session.commit()
                updated_images = []
        if updated_images:
            session.bulk_update_mappings(Image, updated_images)
            session.flush()
        session.commit()

# %% ../nbs/02_alchemy.ipynb 31
def update_images(session, input_dir,
                databases:List[FaceDataBase], 
                attributes: List[str], 
                force_update: bool = False
                ):

    update_functions = {
        'gender': update_gender,
        'age': update_age,
        'emotion': update_emotion,
        'race': update_race
    }

    for attribute in attributes:
        if attribute in update_functions:
            update_functions[attribute](session, input_dir, databases, force_update)

# %% ../nbs/02_alchemy.ipynb 34
def update_cropped_images(session, input_dir:str, force_update: bool = False, serfiq = None):
        
    query = session.query(CroppedImage).join(Detector)
    
    if not force_update:
        query = query.filter(or_(CroppedImage.face_detected == None, CroppedImage.bounding_box == None))

    query_serfiq = query.filter(Detector.name == 'mtcnn_serfiq')
    query_general = query.filter(Detector.name != 'mtcnn_serfiq')

    all_cr_img_serfiq = (query_serfiq.all())
    all_cr_img_general = (query_general.all())

    updated_images = []
    count = 0
    
    if all_cr_img_serfiq:
        # ser_fiq = serfiq
        fill_cropped_image = fill_cropped_image_serfiq
        for cr_img in tqdm(all_cr_img_serfiq, desc='Update cropped images serfiq'):
            fill_cropped_image(cr_img, input_dir, ser_fiq = serfiq)
            updated_images.append(cr_img)
            count += 1
            if count % 100 == 0:
                session.bulk_update_mappings(CroppedImage, updated_images)
                session.flush()
                updated_images = []

    # ser_fiq = None
    fill_cropped_image = fill_cropped_image_general

    for cr_img in tqdm(all_cr_img_general, desc='Update cropped images'):
        fill_cropped_image(cr_img, input_dir, ser_fiq = serfiq)
        session.commit()


# %% ../nbs/02_alchemy.ipynb 35
def update_face_images(session, input_dir:str, force_update: bool = False, serfiq = None):
    update_embeddings_deepface(session, input_dir, force_update)
    update_embeddings_qmagface(session, input_dir, force_update, serfiq = serfiq)
# self.update_confusion_score(force_update)

# %% ../nbs/02_alchemy.ipynb 36
def update_embeddings_deepface(session, input_dir:str, force_update: bool = False):

    query = session.query(FaceImage, EmbeddingModel, Detector, Image) \
        .join(EmbeddingModel) \
        .join(CroppedImage,CroppedImage.croppedImage_id == FaceImage.croppedImage_id) \
        .join(Detector) \
        .join(Image, Image.image_id ==CroppedImage.image_id) \
        .filter(EmbeddingModel.name != 'FaceVACs', EmbeddingModel.name != 'QMagFace', Detector.name != 'mtcnn_serfiq')

    if not force_update:
        query = query.filter(FaceImage.embeddings == None)
    all_face_img = (query.all())

    updated_face_images = []
    count = 0

    for face_img in tqdm(all_face_img, desc='Computing embeddings DeepFace'):
        embedding = DeepFace.represent(face_img.Image.get_image(input_dir), detector_backend=face_img.Detector.name,
                                    model_name=face_img.EmbeddingModel.name, enforce_detection=True)
        face_img.FaceImage.embeddings = embedding
        updated_face_images.append({"faceImage_id": face_img.FaceImage.faceImage_id, "embeddings": face_img.FaceImage.embeddings})
        count += 1
        if count % 100 == 0:
            try:
                session.bulk_update_mappings(FaceImage, updated_face_images)
                session.commit()
                updated_face_images = []
            except:
                session.rollback()
                raise Exception("Error updating embeddings for FaceImages in the database")
    if updated_face_images:
        try:
            session.bulk_update_mappings(FaceImage, updated_face_images)
            session.commit()
        except:
            session.rollback()
            raise Exception("Error updating embeddings for FaceImages in the database")

# %% ../nbs/02_alchemy.ipynb 38
def update_embeddings_qmagface(session, input_dir:str, force_update: bool = False, serfiq = None):

    query = session.query(FaceImage,CroppedImage) \
        .join(EmbeddingModel) \
        .filter(EmbeddingModel.name == 'QMagFace') \
        .join(CroppedImage,CroppedImage.croppedImage_id == FaceImage.croppedImage_id)

    if not force_update:
        query = query.filter(FaceImage.embeddings == None)
    all_face_img = (query.all())

    model = load_model()

    updated_face_images = []
    count = 0

    for face_img in tqdm(all_face_img, desc='Computing embeddings QMagFace'):
        img = face_img.CroppedImage.get_aligned_image(input_dir, ser_fiq = serfiq)
        embedding = compute_qmagface_embeddings(img, model)
        face_img.FaceImage.embeddings = embedding
        updated_face_images.append({"faceImage_id": face_img.FaceImage.faceImage_id, "embeddings": face_img.FaceImage.embeddings})
        count += 1
        if count % 100 == 0:
            try:
                session.bulk_update_mappings(FaceImage, updated_face_images)
                session.commit()
                updated_face_images = []
            except:
                session.rollback()
                raise Exception("Error updating embeddings for FaceImages in the database")
    if updated_face_images:
        try:
            session.bulk_update_mappings(FaceImage, updated_face_images)
            session.commit()
        except:
            session.rollback()
            raise Exception("Error updating embeddings for FaceImages in the database")

# %% ../nbs/02_alchemy.ipynb 40
def update_quality_images(session, input_dir, serfiq=None, force_update: bool = False):
    
    update_ser_fiq(session, input_dir, serfiq = serfiq, force_update=force_update)
    update_tface(session, input_dir,  serfiq = serfiq, force_update=force_update)         

# %% ../nbs/02_alchemy.ipynb 41
def update_ser_fiq(session, input_dir, serfiq = None, force_update: bool = False):
    
    # todo: Now it is only for ArcFace, it should be expanded to other embedding models.
    query = session.query(QualityImage, CroppedImage) \
        .join(QualityModel) \
        .join(FaceImage, FaceImage.faceImage_id == QualityImage.faceImage_id) \
        .join(EmbeddingModel) \
        .join(CroppedImage, CroppedImage.croppedImage_id == FaceImage.croppedImage_id) \
        .filter(EmbeddingModel.name == 'ArcFace',
                QualityModel.name == 'ser_fiq')
    #    .join(Image, Image.image_id == CroppedImage.image_id) \
       

    if not force_update:
        query = query.filter(QualityImage.quality == None)
    all_rows = (query.all())

    # for row in tqdm(all_rows[:5], desc='TRIM Computing SER-FIQ quality'):
    for row in tqdm(all_rows, desc='Computing SER-FIQ quality'):             

        aligned_img = row.CroppedImage.get_aligned_image(input_dir, ser_fiq=serfiq) 
        quality = serfiq.get_score(aligned_img, T=100)
        
        row.QualityImage.quality = quality
        session.commit()

# %% ../nbs/02_alchemy.ipynb 42
def update_tface(session, input_dir, serfiq, force_update: bool = False):
    ser_fiq = serfiq

    net, gpu_available = get_network()

    # todo: Now it is only for ArcFace, it should be expanded to other embedding models. 
    # Is it ArcFace or another face recognition model?
    
    query = session.query(QualityImage, CroppedImage) \
        .join(QualityModel) \
        .join(FaceImage, FaceImage.faceImage_id == QualityImage.faceImage_id) \
        .join(EmbeddingModel) \
        .join(CroppedImage, CroppedImage.croppedImage_id == FaceImage.croppedImage_id) \
        .filter(EmbeddingModel.name == 'ArcFace', 
                QualityModel.name == 'tface')
        # .join(Image, Image.image_id == CroppedImage.image_id) 
        

    if not force_update:
        query = query.filter(QualityImage.quality == None)
    all_rows = (query.all())

    # for row in tqdm(all_rows[:5], desc='TRIM: Computing TFace quality'): 
    for row in tqdm(all_rows, desc='Computing TFace quality'):             

        aligned_img = row.CroppedImage.get_aligned_image(input_dir, ser_fiq=serfiq) 
        quality = compute_tf_quality(aligned_img, net, gpu_available=gpu_available)             
        
        row.QualityImage.quality = quality
        session.commit()
