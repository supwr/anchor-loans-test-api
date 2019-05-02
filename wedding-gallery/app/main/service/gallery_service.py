from main.database import mongo
from main.s3 import client
import datetime
import uuid
import os


class GalleryService:

    @staticmethod
    def get_image_by_id(id):
        return mongo.db.gallery.find_one({"_id": id})

    @staticmethod
    def list_approved_images():
        return mongo.db.gallery.find({"approved": True})

    @staticmethod
    def list_all_images():
        return mongo.db.gallery.find()

    @staticmethod
    def new_image(file, user_id):
        filename, file_extension = os.path.splitext(file.filename)
        filename = '%s%s' % (str(uuid.uuid4()), file_extension)

        image = {
            "filename": filename,
            "approved": False,
            "createdBy": user_id,
            "createdAt": datetime.datetime.utcnow()
        }

        client.upload_fileobj(file, 'capybaraweddingapp', image["filename"])

        return mongo.db.gallery.insert(image)

    @staticmethod
    def remove_image(image):
        client.delete_object(Bucket='capybaraweddingapp', Key=image['filename'])
        return mongo.db.gallery.remove({"_id": image["_id"]})

    @staticmethod
    def approve_image(user_id, image_id):
        image = {
            "approved": True,
            "disapprovedBy": None,
            "disapprovedAt": None,
            "approvedBy": user_id,
            "approvedAt": datetime.datetime.utcnow()
        }

        return mongo.db.gallery.update_one({"_id": image_id}, {"$set": image})

    @staticmethod
    def disapprove_image(user_id, image_id):
        image = {
            "approved": False,
            "disapprovedBy": user_id,
            "disapprovedAt": datetime.datetime.utcnow(),
            "approvedBy": None,
            "approvedAt": None
        }

        return mongo.db.gallery.update_one({"_id": image_id}, {"$set": image})

    @staticmethod
    def like_image(user_id, image_id):

        if mongo.db.gallery.find_one({"_id": image_id, "likes.user": user_id}) is None:
            return mongo.db.gallery.update_one({"_id": image_id}, {"$push": {"likes": {"user": user_id}}})

        return mongo.db.gallery.update_one({"_id": image_id}, {"$pull": {"likes": {"user": user_id}}})

