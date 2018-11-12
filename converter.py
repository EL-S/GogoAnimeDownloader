import os
import shutil
import glob
from threading import Thread
import time
import os.path
import psutil

root_dir = "Episodes/"
output_format = ".mkv"
overwrite = True
keep_source_stream=False
folders_to_delete = []

def check_for_file(out_file=None,directory=None,episode_file_name=None,keep_source_stream=None,single=False):
     if single:
          while True:
               if os.path.exists(out_file):
                    if keep_source_stream == False:
                         time.sleep(1)
                         try:
                              shutil.rmtree(directory)
                              break
                         except Exception as e:
                              #print("Couldn't Delete Source Files!",e)
                              pass
                    else:
                         break
               
               else:
                    time.sleep(1/10)
          print("Removed Source File!\n")
     else:
          print("Be patient for the deletion to occur!")
          time.sleep(10)
          for folder in folders_to_delete:
               while True:
                    out_file = folder[0]
                    directory = folder[1]
                    episode_file_name = folder[2]
                    keep_source_stream = folder[3]
                    if os.path.exists(out_file):
                         if keep_source_stream == False:
                              try:
                                   shutil.rmtree(directory)
                                   break
                              except Exception as e:
                                   pass
                                   #print("Couldn't Delete Source Files!",e)
                         else:
                              break
                    
                    else:
                         time.sleep(1/10)
          print("Removed Source File(s)!\n")
                    

def convert_directory(root_dir,output_format=".mkv",overwrite=None,keep_source_stream=False):
     global folders_to_delete
     folders_to_delete = []
     for filename in glob.iglob(root_dir + '**/playlist.m3u8', recursive=True):
          convert_file(filename,output_format,overwrite,keep_source_stream,single=False)
     if folders_to_delete != []:
          check_for_file(single=False)
     else:
          print("Nothing to convert!")

def convert_file(path,output_format=".mkv",overwrite=None,keep_source_stream=False,single=True):
     print("Converting...")
     path = (r'{}'.format(path)) #use a string literal to negate escaped characters
     path = path.replace("\\","/") #replace backwards slash with forwards slash
     folder_name = path.split("/")[-2]
     directory = "/".join(path.split("/")[:-1])
     in_file = path.split("/")[-1:][0]
     out_file = "../"+folder_name+output_format
     if "Episode" in out_file:
          fancy_formatting = folder_name.split("Episode")
          fancy_formatting = fancy_formatting[0]+"- EP"+fancy_formatting[1].strip()
          out_file = "../"+fancy_formatting+output_format
     if os.path.exists(directory):
          convert_command(directory,in_file,out_file,output_format,overwrite,keep_source_stream,single)
     else:
          print("Nothing to convert!")

def convert_command(directory, in_file, out_file, output_format=".mkv", overwrite=None, keep_source_stream=False, single=True):
     global folders_to_delete
     if overwrite:
          print("Overwriting",out_file)
          overwrite_str = "-y "
     else:
          print("No-Overwriting...")
          overwrite_str = ""
     command = 'cd "'+directory+'" && start /min ffmpeg '+overwrite_str+'-i "'+in_file+'" -acodec copy -bsf:a aac_adtstoasc -vcodec copy "'+out_file+'"'
     try:
          episode_file_name = out_file.split("/")[1]
          #print("Creating",episode_file_name)
          os.system(command) #command to create the file
          anime_folder = "/".join(directory.split("/")[:-1])
          out_file_relative = anime_folder+"/"+episode_file_name
          if single:
               file_delete = Thread(target = check_for_file, args=(out_file_relative,directory,episode_file_name,keep_source_stream,single))
               file_delete.start()
          else:
               folders_to_delete.append([out_file_relative,directory,episode_file_name,keep_source_stream])
               
     except:
         print("Something went wrong converting!")

#convert_directory(root_dir,overwrite=overwrite)
#location = input("Input: ")
#location2 = ("%r"%location)[1:][:-1]
#location = "Episodes\Accel World\Accel World Episode 1 English Subbed\playlist.m3u8"
#print(location)
#convert_directory("Episodes\\",overwrite=True,keep_source_stream=False)
#convert_file("Episodes\Accel World\Accel World Episode 1 English Subbed\playlist.m3u8",overwrite=True,keep_source_stream=False)
