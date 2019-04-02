# -----------------------------------------------
# Setup global defaults for the analysis project
# -----------------------------------------------

# The first set of variables involve the Azure blob storage account and key containing the photosphere image data. 
# Using these two values, we create a blobService that can be used (parsed) in consequent functions and operations.

# Also, in order to run the Azure Cognitive Services REST API, the following values must be provided:
#   a. The Azure region for which the API is configured, and;
#   b. The API key generated for the Azure Cognitive Services Computer Vision service.
# These two values, are then parsed for use in the rest of the code and functions.

import os, http.client
# Set maximum number of http requests
http.client._MAXHEADERS = 5000


# Setup account and key for the Azure blob storage containing the photosphere images.
blobAccount = 'azmlstorageblob'
blobKey = 'pBG54bJUphLDEcuhob7gFywUHzRwFEnw6ZqMVpM/QeIOaGkx7SO3uTMd2lZ783Ocy0vkxiTw+70eFhqeB4fwEw=='
containerName = 'photospheres'

# Setup region and key for the Azure vision client API
apiRegion = 'westus2'
apiKey = 'd0d6e0b08528494587e8fb0e5efee409'


computer = os.environ['COMPUTERNAME']
if computer == "SRVYGS046C":
    prjPath = r"C:\Users\OCPWAlexandridisK\source\repos\ktalexan\ML-Vision-Photospheres"
elif computer == "DRK01":
    prjPath = r"C:\Users\ktale\source\repos\ktalexan\ML-Vision-Photospheres"
os.chdir(prjPath)

%run AzureCognitiveVisionRest.py
%load AzureCognitiveVisionRest.py
az = AzCognVisionRest(blobAccount, blobKey, apiRegion, apiKey, containerName)

# Class function tests -- all working fine.
test1 = az.check_degrees(355.25, 22.5)
az.check_cardinality(test1)
az.check_cardinality(360)
az.get_dir(6041009.706, 2242810.667)
az.convert_stateplane(6041009.706, 2242810.667, 106.627)
dtobj = az.time_convert('181204_182503563.jpg', 236745.38592)
blobtest = az.get_blob_list()
for blob in blobtest:
    print(blob.name)


az.update_blob_metadata(metadata = 'CameraMetadata.xlsx')

blobList = az.get_blob_list()
az.process_cardinal_images(blobList[0], containerIn = containerName, containerOut= 'cardinal')
for blob in tqdm(blobList):
    az.process_cardinal_images(blob, containerIn = containerName, containerOut= 'cardinal')

