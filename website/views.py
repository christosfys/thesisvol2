from multiprocessing.spawn import prepare
from django.shortcuts import render
import os
import datetime
import requests
import shutil
from django.conf import settings
from django.http import HttpResponse, FileResponse
from django.http import StreamingHttpResponse
import json
import re
import mlflow
from mlflow import MlflowClient
from . models import Task_Category
import qrcode
import base64
from PIL import Image, ImageDraw, ImageFont
import io
import re

#MLflow parameter
MLFLOW_URI = 'http://195.130.121.234:8085/'
os.environ['MLFLOW_TRACKING_URI'] = MLFLOW_URI

# os.environ['AWS_ACCESS_KEY_ID'] = 'admin'
# os.environ['AWS_SECRET_ACCESS_KEY'] = 'admin8888'
# os.environ['MLFLOW_S3_ENDPOINT_URL'] = 'http://195.130.121.234:8089/'

# Create an instance of the MlflowClient class
client = mlflow.MlflowClient()

# Views

def homepage(request):
    tasks = Task_Category.objects.all()
    # Retrieve the list of experiments and runs from the MLflow server
    experiments = client.search_experiments()
    filtered_experiments = []
    filtered_models = []
    # runs = client.search_runs(experiment_ids=[e.experiment_id for e in experiments])

    # model = client.get_registered_model('DVC_Mlflow')
    models = client.search_registered_models()
    for t in tasks:
        for model in models:
            if model.tags.get('Task') == str(t):
                filtered_experiments.append(model)
                model = client.get_registered_model(model.name)
                # author = model.tags.get('author')
                all_tags = model.tags
                # print(all_tags)
                last_updated_timestamp = model.last_updated_timestamp
                last_updated_datetime = datetime.datetime.fromtimestamp(last_updated_timestamp/1000.0)
                last_updated_str = last_updated_datetime.strftime('%Y-%m-%d ')
                latest_version = model.latest_versions[0]
                version = latest_version.version
                publisher = latest_version.tags.get('publisher')
                # experiment_id = latest_version.tags.get('Experiment_ID')
                
                regex = re.compile(r'((http(s)?)|(git@[\w\.]+))(:(//)?)([\w\.@\:/\-~]+)(\.git)?(/)?', re.IGNORECASE)
                qr_url = latest_version.tags.get('Git repo')

                if re.match(regex, qr_url) is not None:
                    qr_code = qr_url

                    qr = qrcode.QRCode(
                            version=1,
                            box_size=10,
                            border=5)
                    qr.add_data(qr_code)
                    qr.make(fit=True)

                    img = qr.make_image(fill='black', back_color='white')


                    # Convert PIL.Image to bytes
                    byte_stream = io.BytesIO()
                    img.save(byte_stream, format='PNG')
                    byte_stream.seek(0)
                    image_bytes = byte_stream.getvalue()
                    b64 = base64.b64encode(image_bytes).decode("utf-8")
                    name_preview = latest_version.tags.get('Name')
                    print(model.name)
                    print(name_preview)
                    learning_prob = latest_version.tags.get('Learning Problem')
                    filtered_models.append({
                        'name': model.name,
                        'name_preview': name_preview,
                        'qr_code': b64,
                        'learning_problem': learning_prob,
                        'publisher': publisher,
                        'version': version,
                        'last_update': last_updated_str,
                        'task': model.tags.get('Task')
                    })
                
                else:

                    # Create an image with the author's name when qr_code is None
                    image_width = 100
                    image_height = 100
                    background_color = (255, 255, 255)
                    text_color = (0, 0, 0)

                    image = Image.new("RGB", (image_width, image_height), background_color)
                    draw = ImageDraw.Draw(image)

                    font = ImageFont.load_default()
                    text = latest_version.tags.get('Author')

                    text_width = draw.textlength(text, font=font)
                    text_height = font.getbbox(text)[-1]  # get the height of the font
                    text_x = (image_width - text_width) // 2
                    text_y = (image_height - text_height) // 2

                    draw.text((text_x, text_y), text, fill=text_color, font=font,align='center')

                    # Convert the image to bytes
                    img_byte_array = io.BytesIO()
                    image.save(img_byte_array, format='PNG',optimize=True,compress_level=5)
                    img_byte_array.seek(0)

                    img = Image.open(img_byte_array)
                    
                    # Convert PIL.Image to bytes
                    byte_stream = io.BytesIO()
                    img.save(byte_stream, format='PNG',optimize=True,compress_level=5)
                    byte_stream.seek(0)

                    image_bytes = byte_stream.getvalue()
                    b64 = base64.b64encode(image_bytes).decode("utf-8")
                    name_preview = latest_version.tags.get('Name')
                    print(model.name)
                    print(name_preview)
                    learning_prob = latest_version.tags.get('Learning Problem')
                    filtered_models.append({
                        'name': model.name,
                        'name_preview': name_preview,
                        'qr_code': b64,
                        'learning_problem': learning_prob,
                        'publisher': publisher,
                        'version': version,
                        'last_update': last_updated_str,
                        'task': model.tags.get('Task')
                    })
                

    context={
        'task':tasks,
        'experiments': filtered_models, 
    }
    return render(request,"base.html",context)

def download_model(request,model_name):
    # print(model_name)
    model = client.get_registered_model(model_name)
    latest_version = model.latest_versions[0]
    repo_url = latest_version.tags.get('Git repo')
    repo_name = os.path.basename(repo_url)
    # print(repo_url)
    print(repo_name)
    repo_name_zip = repo_name + "-master.zip"
    file_path_zip = repo_name + ".zip" 
    download_url = f"{repo_url}/-/archive/master/{repo_name_zip}"
    response = requests.get(download_url, stream=True)

    if response.status_code == 200:
        # Create a directory for the extracted files
        dir_path = os.path.join(settings.MEDIA_ROOT, 'models_download')
        os.makedirs(dir_path, exist_ok=True)
        
        # Save the zip file to the server
        zip_file_path = os.path.join(dir_path, '{file_path_zip}')
        with open(zip_file_path, "wb") as f:
            response.raw.decode_content = True
            shutil.copyfileobj(response.raw, f)

        # Return the file as a response
        def file_iterator(file_name, chunk_size=8192):
            with open(file_name, "rb") as f:
                while True:
                    chunk = f.read(chunk_size)
                    if not chunk:
                        break
                    yield chunk

                   
        file_path = os.path.join(dir_path, file_path_zip)
        file_size = os.path.getsize(file_path)
        response = StreamingHttpResponse(file_iterator(file_path))
        response['Content-Length'] = file_size
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(file_path_zip)
        return response
    else:
        return HttpResponse("Failed to download file. Status code: {}".format(response.status_code))
   

def category(request):
    # Retrieve the list of experiments and runs from the MLflow server
    experiments = client.search_experiments()
    filtered_experiments = []
    filtered_models = []
    # runs = client.search_runs(experiment_ids=[e.experiment_id for e in experiments])

    # model = client.get_registered_model('DVC_Mlflow')
    models = client.search_registered_models()
    for model in models:
        if model.tags.get('task') == 'Segmentation':
            filtered_experiments.append(model)
            model = client.get_registered_model(model.name)
            # author = model.tags.get('author')
            all_tags = model.tags
           
            last_updated_timestamp = model.last_updated_timestamp
            last_updated_datetime = datetime.datetime.fromtimestamp(last_updated_timestamp/1000.0)
            last_updated_str = last_updated_datetime.strftime('%Y-%m-%d ')
            latest_version = model.latest_versions[0]
            version = latest_version.version
            author = latest_version.tags.get('author')
            description = latest_version.description
            filtered_models.append({
            'name': model.name,
            'description': description,
            'author': author,
            'version': version,
            'last_update': last_updated_str
        })
    context = {
        'experiments': filtered_models,        
    }

    # print(runs)
    return render(request,"category.html", context)

def model_details(request, model_name):
    run_names = []
    
    model_info = {}
    dataset_info = {}
    model = client.get_registered_model(model_name)
    model
    print(model)
    latest_version = model.latest_versions[0]
    all_keys = list(latest_version.tags.keys())
    standard_keys = ['Algorithm','Ethical concerns','Learning Method','Learning Problem','Name','Risk Assessment','Storage','author','Metric','Task','Framework','git repo']
    other_keys = [key for key in all_keys if key not in standard_keys]
    
    try:
        source_run_id = latest_version.run_id
        run_meta = client.get_run(source_run_id)
        implementation = run_meta.data.tags["mlflow.source.git.commit"]
    except:
        implementation = None
    # Date
    release_date_timestamp = model.last_updated_timestamp
    release_date_timestamp = datetime.datetime.fromtimestamp(release_date_timestamp/1000.0)
    release_date_timestamp = release_date_timestamp.strftime('%Y-%m-%d ')
    model_info['Task_name']=model.tags.get('Task')
    model_info['Download_Name'] = model.name
    model_info['Name'] = latest_version.tags.get('Name')
    model_info['Author'] = latest_version.tags.get('Author')
    model_info['Source Run ID'] = latest_version.tags.get('Experiment_run_id')
    model_info['Version'] = latest_version.version
    model_info['Release Date'] = release_date_timestamp
    model_info['Model UUID'] = latest_version.tags.get('model_uuid')
    model_info['Description'] = latest_version.tags.get('description')
    model_info['Publisher'] = latest_version.tags.get('publisher')
    model_info['Learning Problem'] = latest_version.tags.get('Learning Problem')
    model_info['Learning Method'] = latest_version.tags.get('Learning Method')
    model_info['Algorithm'] = latest_version.tags.get('Algorithm')
    model_info['Framework'] = latest_version.tags.get('Algorithm')
    model_info['Framework'] = model_info['Framework'].replace('$', ': ')
    model_info['Model Hyperparameters'] = ', '.join([f"{key}:{latest_version.tags[key]}" for key in other_keys])
    model_info['License'] = "NC-SA-CC-BY"
    model_info['Storage'] = latest_version.tags.get('Storage')
    model_info['Ethical Concerns'] = latest_version.tags.get('Ethical concerns')
    model_info['Risk Assessment'] = latest_version.tags.get('Risk Assessment')
    model_info['Experiment Name'] = latest_version.tags.get('Experiment_name')
    model_info['Git Repo'] = latest_version.tags.get('Git repo')
    model_info['Metric Score'] = latest_version.tags.get('Metric score')
    model_info['Input Channels'] = latest_version.tags.get('Number_input_channels')
    model_info['Number Labels'] = latest_version.tags.get('Number_labels')
    model_info['Activation'] = latest_version.tags.get('activation')
    model_info['Layer Activation'] = latest_version.tags.get('layer_activation')
    model_info['Batch Size'] = latest_version.tags.get('batch_size')
    model_info['Device'] = latest_version.tags.get('device')
    model_info['Epoch'] = latest_version.tags.get('epoch')
    model_info['Filters'] = latest_version.tags.get('filters')
    model_info['Loss'] = latest_version.tags.get('loss')
    model_info['Metric'] = latest_version.tags.get('metric')
    model_info['Optimiser'] = latest_version.tags.get('optimiser')

    

    hyperparameters_dict = {}
    for key in other_keys:
        value = latest_version.tags.get(key)
        if value:
            if "[" in value and "]" in value:
                value = [int(x) for x in value.strip("[]").split(", ")]
            elif value == "True":
                value = True
            elif value == "False":
                value = False
            else:
                value = str(value)
            hyperparameters_dict[key] = value

    model_info['Model Hyperparameters'] = hyperparameters_dict
    # print(model_info['Model Hyperparameters'] )

    # Experiment ID
    mlflow_experiment_id = latest_version.tags.get('Experiment_run_id')
    
    run = client.get_run(mlflow_experiment_id)

    run_pipeline = run.data.tags['pipeline'].split(";")
    dictionaries = {}
    suffix = "_run_id"
    pipeline_run_id = [value + suffix for value in run_pipeline] 
    
    for stage in pipeline_run_id:
        dictionaries[stage] = {}
        dictionaries[stage]['ID'] = run.data.tags[stage]
        stage_run = client.get_run(dictionaries[stage]['ID'])
        if  stage_run.data.tags.get("depdata"):
            stage_dataset = stage_run.data.tags["depdata"].split("$")
            dictionaries[stage]['Input_Dataset_ID'] = stage_dataset[1]
            dictionaries[stage]['Input_Dataset_Path'] = stage_dataset[0]
        if  stage_run.data.tags.get("depcode"):    
            stage_source = stage_run.data.tags["depcode"].split("$")
            dictionaries[stage]['Source_Code_ID'] = stage_source[1]
            dictionaries[stage]['Source_Code_Path'] = stage_source[0]
        if stage_run.data.tags["task"]:
            dictionaries[stage]['task'] = stage_run.data.tags["task"]
        if stage_run.data.tags["out"]:
            stage_out = stage_run.data.tags["out"].split("$")
            dictionaries[stage]['Output_Dataset_ID'] = stage_out[1]
            dictionaries[stage]['Output_Dataset_Path'] = stage_out[0]
        if stage_run.data.tags["framework"]:
            dictionaries[stage]['framework'] = stage_run.data.tags["framework"].replace('$', ': ')
        dictionaries[stage]['params'] = stage_run.data.params

    #Dataset info from parent id
    dataset_info = {key:value for key,value in run.data.tags.items()
                        if key.startswith('dataset_')
                    }
    
    dataset_creation_date = run.data.tags["dataset_created_tr"].split(" ")
    dataset_info['dataset_creation'] = dataset_creation_date[0]
    dataset_info["dataset_created_tr"] = dataset_info["dataset_created_tr"].split(" ")[0]
    dataset_info["dataset_modified_tr"] = dataset_info["dataset_modified_tr"].split(" ")[0]
    dataset_info["dataset_modified"] = dataset_info["dataset_modified"].split(" ")[0]
    dataset_info['dataset_size'] = round(int(run.data.tags["dataset_size"])/(1024 * 1024))
    dataset_info['dataset_pipeline'] = run.data.tags["pipeline"]

    regex = re.compile(r'((http(s)?)|(git@[\w\.]+))(:(//)?)([\w\.@\:/\-~]+)(\.git)?(/)?', re.IGNORECASE)
    
    download_link=model_info['Git Repo']
    if re.match(regex, download_link) is not None:
        splitted = download_link.split("/")
        download_link = download_link + "/-/archive/master/"+splitted[4]+"-master.zip"
    else:
        download_link = None
    
    print(download_link)

    
    context = {
        'task_name':model_info['Task_name'],
        'download_model': model_info['Download_Name'],
        'model_author': model_info['Author'],
        'model_name': model_info['Name'],
        'model_source_run_id': model_info['Source Run ID'],
        'model_version': model_info['Version'],
        'model_publisher': model_info['Publisher'],
        'model_storage': model_info['Storage'],
        'model_uuid': model_info['Model UUID'],
        'model_descr': model_info['Description'],
        'model_license': model_info['License'],
        'model_release_date': model_info['Release Date'],
        'model_risk_assesment':  model_info['Risk Assessment'],
        'model_learning_problem': model_info['Learning Problem'],
        'model_learning_method': model_info['Learning Method'],
        'model_ethical_con': model_info['Ethical Concerns'],
        'model_git_repo': model_info['Git Repo'],
        'model_metric_score': model_info['Metric Score'],
        'model_input_ch': model_info['Input Channels'],
        'model_number_labels': model_info['Number Labels'],
        'model_activation': model_info['Activation'],
        'model_hyperparameters': model_info['Model Hyperparameters'],
        'model_algorithm': model_info['Algorithm'],
        'model_layer_activation': model_info['Layer Activation'],
        'model_batch_size':model_info['Batch Size'],
        'model_framework': model_info['Framework'],
        'model_implementation': implementation,
        'model_device':  model_info['Device'],
        'model_epoch': model_info['Epoch'],
        'model_filters': model_info['Filters'],
        'model_loss': model_info['Loss'],
        'model_metric': model_info['Metric'],
        'model_optimiser': model_info['Optimiser'],
        'dictionaries' : dictionaries,
        'download_model' : download_link,
    }
    print(dictionaries)

    context.update(dataset_info)
 
    return render(request, 'model_details_new.html', context)
    


def get_run_sequence(client, parent_run_id):
    """
    Returns a list of run IDs in the order in which they were executed, starting with the specified parent run ID
    """
    run_sequence = [parent_run_id]
    
    # get the parent run
    parent_run = client.get_run(parent_run_id)
    
    # get the child runs
    child_runs = client.search_runs(experiment_ids=[parent_run.info.experiment_id], filter_string=f"tags.mlflow.parentRunId = '{parent_run_id}'")
    
    # sort the child runs by start time
    child_runs.sort(key=lambda r: r.info.start_time)
    
    # recursively process each child run
    for child_run in child_runs:
        previous_run_id = child_run.data.tags.get("previous_run_id")
        if previous_run_id:
            run_sequence.extend(get_run_sequence(client, previous_run_id))
        run_sequence.append(child_run.info.run_id)
    
    return run_sequence


# define a function to rename the key recursively
def rename_key(data, key_path, new_name):
    if len(key_path) == 1:
        data[new_name] = data.pop(key_path[0])
    else:
        rename_key(data[key_path[0]], key_path[1:], new_name)

# define a function to update the value of a key recursively
def update_key(data, key_path, new_value):
    if len(key_path) == 1:
        data[key_path[0]] = new_value
    else:
        update_key(data[key_path[0]], key_path[1:], new_value)


def role_display(request):
    
 
    return render(request, 'roles.html')

