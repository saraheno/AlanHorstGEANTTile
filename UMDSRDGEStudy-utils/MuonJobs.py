#!/usr/bin/python
import os, sys
import shlex, subprocess
from datetime import datetime, date, time
from time import sleep
import shutil
import numpy as np   
#sys.path.append(os.path.abspath(os.path.curdir))

JobTime = datetime.now()
fTag = JobTime.strftime("%Y%m%d_%H%M%S")
sTag = "DataCollectionMuonTotalEneUnirr"
dirname = "jobs/%s_%s"%(sTag,fTag)
DetType = "0" #Tile
logFile = "0606.log"

try:
    os.makedirs(dirname)
except:
    pass

ProdTag = "Run4_20170606"
OutDir  = "/home/ahorst/UMDSRDGEStudy-build/Absdata"
WorkDir = "/home/ahorst/UMDSRDGEStudy-build"

try:
    os.makedirs(OutDir)
except:
    pass

try:
    os.makedirs(OutDir+"/"+ProdTag)
except:
    pass

try:
    os.makedirs(OutDir+"/"+ProdTag+"/logs")
except:
    pass



#########################################
#make sure OutDir is the same in main.cc
#########################################
condor_script_template = """
universe = vanilla
Executable = ./CMS.sh
+IsLocalJob = true
Should_transfer_files = NO
Requirements = TARGET.FileSystemDomain == "privnet"
Output = %(OUTDIR)s/%(MYPREFIX)s/logs/%(FILENAME)s_sce_$(cluster)_$(process).stdout
Error  = %(OUTDIR)s/%(MYPREFIX)s/logs/%(FILENAME)s_sce_$(cluster)_$(process).stderr
Log    = %(OUTDIR)s/%(MYPREFIX)s/logs/%(FILENAME)s_sce_$(cluster)_$(process).condor
Arguments = %(WORKDIR)s %(INPUT)s %(FILENAME)s %(DETTYPE)s
Queue 1
 
"""
######################%(WORKDIR)s %(INPUT)s %(FILENAME)s %(DETTYPE)s###################
# %(OUTDIR)s/%(MYPREFIX)s/

#starting wavelenght
#Initial = 3.0538
#array that contains the different wavelengths being tested                          
#Arr = [3.0538, 3.0463, 3.0388, 3.0314, 3.024, 3.0166, 3.0093, 3.002, 2.9948, 2.9876]
#3.5424, 3.4925, 3.444, 3.3968, 3.3509, 3.3062, 3.2627, 3.2204, 3.1791, 3.1388]
#,]
#3.1309, 3.123, 3.1152, 3.1074, 3.0996, 3.0919, 3.0842, 3.0765, 3.0689, 3.0613
#for q in range(0,len(Arr)):

 #initial absorption length NOTE: if using 1 or 10 make sure to use 10.0 or 1.0 as there are other instances of the strings
 # 1 and 10 in the file
AbsIN = 0
EnIN = 3.5424

#final absorption length  
AbsFI = 0
EnFI = 2.7552

#total number of jobs being submitted 
jobNUM = 1


#array that contains the different abs lengths being tested                          
Arr = np.linspace(AbsIN,AbsFI,num=jobNUM)
EnArr = np.linspace(EnIN,EnFI,num=jobNUM)

#for q in range(len(EnArr)):
for q in range(len(Arr)):
    
    # Creating new file                                                              
    shutil.copy2('photontestMuon.mac', 'photest' '%s' '.mac' % q)

    # Reading in the file                                                            
    with open('photest' '%s' '.mac' % q, 'r') as file :
        filedata = file.read()


    # Writing out the new file                                                       
    with open('photest' '%s' '.mac' % q, 'w') as file:
        file.write(filedata)

    # Defining the infile                                                            
    InFile = 'photest' '%s' '.mac' % q 
    
    kw = {}

    kw["MYPREFIX"]  = ProdTag
    kw["WORKDIR"]   = WorkDir
    kw["OUTDIR"]    = OutDir
    kw["INPUT"]     = InFile
    kw["FILENAME"]  = sTag
    kw["DETTYPE"]   = DetType
    kw["LOGFILE"]   = logFile

    script_str = condor_script_template % kw
    f = open("%s/condor_jobs_%s_G4Sim.jdl"%(dirname,sTag), 'w')
    f.write(script_str)
    f.close()

    condorcmd = "condor_submit %s/condor_jobs_%s_G4Sim.jdl"%(dirname,sTag)
    print 'condorcmd: ', condorcmd
    print ('Executing condorcmd %s' % str(q))

    p=subprocess.Popen(condorcmd, shell=True)
    p.wait()
   
        
    print "\n"
    print "Histos output dir: %s/%s"%(OutDir,ProdTag)

