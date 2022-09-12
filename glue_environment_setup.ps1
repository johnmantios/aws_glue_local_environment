$AWS_CREDENTIALS_LOCATION = ""
$JUPYTER_WORKSPACE_LOCATION = ""

$Env:AWS_ACCESS_KEY_ID = ""
$Env:AWS_SECRET_ACCESS_KEY = ""
$Env:AWS_DEFAULT_REGION = ""
$Env:AWS_PROFILE = ""


docker run -it -v ${AWS_CREDENTIALS_LOCATION}:/home/glue_user/.aws/ -v ${JUPYTER_WORKSPACE_LOCATION}:/home/glue_user/workspace/jupyter_workspace/ -e AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} -e AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} -e AWS_DEFAULT_REGION=${AWS_DEFAULT_REGION} -e AWS_PROFILE=${AWS_PROFILE} -e DISABLE_SSL=true --rm -p 4040:4040 -p 18080:18080 -p 8998:8998 -p 8888:8888 --name glue_jupyter_lab john-glue:latest /home/glue_user/jupyter/jupyter_start.sh
