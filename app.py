"""
Routes and views for the flask application.
"""
from flask import Flask
app = Flask(__name__, template_folder= "template")

from datetime import datetime
from datetime import timedelta
from azure.storage.blob import generate_container_sas, ContainerSasPermissions
from azure.storage.blob import generate_blob_sas, BlobSasPermissions
from flask import render_template


account_name = "cdnstore1"
account_key = "iM7sub7rvl+lBdORwaq9u5KWPiN3Q2h5sYopVxyiAbsemOkedIPeSrnmEQWeIICS32HNyznhzIO8Zol5A55BGw=="
container_name = "images"

#using generate_container_sas
def get_img_url_with_container_sas_token(blob_name):
    container_sas_token = generate_container_sas(
        account_name=account_name,
        container_name=container_name,
        account_key=account_key,
        permission=ContainerSasPermissions(read=True),
        expiry=datetime.utcnow() + timedelta(hours=1)
    )
    blob_url_with_container_sas_token = f"https://{account_name}.blob.core.windows.net/{container_name}/{blob_name}?{container_sas_token}"
    return blob_url_with_container_sas_token

#using generate_blob_sas
def get_img_url_with_blob_sas_token(blob_name):
    blob_sas_token = generate_blob_sas(
        account_name=account_name,
        container_name=container_name,
        blob_name=blob_name,
        account_key=account_key,
        permission=ContainerSasPermissions(read=True),
        expiry=datetime.utcnow() + timedelta(hours=1)
    )
    blob_url_with_blob_sas_token = f"https://{account_name}.blob.core.windows.net/{container_name}/{blob_name}?{blob_sas_token}"
    return blob_url_with_blob_sas_token

@app.route("/showimg")
@app.route("/showimg/<blob_name>")
def showimg(blob_name="Beauty.JPG"):
    img_url_with_sas_token = get_img_url_with_blob_sas_token(blob_name)
    return render_template('index.html',title='Home Page',img_url_with_sas_token=img_url_with_sas_token)


if __name__ == "__main__":
    app.run(debug=True)




