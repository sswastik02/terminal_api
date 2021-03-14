from django.shortcuts import render

import subprocess,os
from rest_framework import generics, response, status
from .serializers import BashSerializer
from .models import command_response


init_dir=os.getcwd()
# Create your views here.
class BashView(generics.ListAPIView):
    queryset = command_response.objects.all()
    serializer_class = BashSerializer
    def get(self, request, format=None):
        command = command_response.objects.all()
        serializer = BashSerializer(command, many=True)
        return response.Response(serializer.data)

    def post(self, request, format=None):
        serializer = BashSerializer(data=request.data)
        username=request.user.username if request.user.is_authenticated else 'guest_user'
        if not os.path.isdir(init_dir+'/'+username):
            create_user_dir=subprocess.run('mkdir {}'.format(username),shell=True,text=True,capture_output=True)
        if not init_dir+'/'+username in os.getcwd():
            os.chdir(init_dir+'/'+username)
        err,out='',''
        if serializer.is_valid():
            a=dict()
            a.update(serializer.validated_data)
            run_command=serializer.validated_data['command']
            if 'cd ' in run_command:                      #subprocess.run cwd changes for an instant executes the command and returns back to working directory
                dir=run_command[3:]                                  
                if os.path.isdir(dir):          
                    os.chdir(dir)
                    if init_dir+'/'+username not in os.getcwd():
                        os.chdir(init_dir+'/'+username)
                        err='Permission Denied'
                elif os.path.exists(dir):
                    err='bash: cd: {}: Not a directory'.format(dir)  #'\''+dir+'\''
                else:
                    err='No such file or directory: {}'.format(dir) #'\''+dir+'\''
            else:
                process=subprocess.run(a['command'],shell=True,text=True,capture_output=True)
                out,err=process.stdout,process.stderr
            a['response']=out if err == '' else err
            a['response']=a['response'].replace(init_dir,'')
            serializer.save(response=a['response'])
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request,format=None):
        commands = command_response.objects.all()
        commands.delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT) 