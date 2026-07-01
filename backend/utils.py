import uuid
import os

def generate_id():

    return str(uuid.uuid4())


def ensure_folder(path):

    if not os.path.exists(path):

        os.makedirs(path)