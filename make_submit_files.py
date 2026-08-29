import os

template_40gb = """#vllm server submit script for V100 32GB / A100 40GB GPUs (tony-1/2/4)
universe                = vanilla
initialdir              = /nethome/USERNAME/vllm_server
executable              = src/vllm_server/start_vllm/start_vllm_2x40gb.sh
output	                = /scratch/USERNAME/vllm_server/run.sh.$(ClusterId).$(Year)_$(Month)_$(Day)_$(SUBMIT_TIME).out
error                   = /scratch/USERNAME/vllm_server/run.sh.$(ClusterId).$(Year)_$(Month)_$(Day)_$(SUBMIT_TIME).err
log                     = /scratch/USERNAME/vllm_server/run.sh.$(ClusterId).$(Year)_$(Month)_$(Day)_$(SUBMIT_TIME).log
request_CPUs            = 16
request_memory          = 150G
request_GPUs            = 2
requirements            = (GPUs_GlobalMemoryMb >= 32000) && (TARGET.UidDomain == "coli.uni-saarland.de") && (TARGET.Machine != "tony-3.coli.uni-saarland.de")
 
getenv                  = True
+WantGPUHomeMounted     = true

queue 1
"""

template_80gb = """#vllm server submit script for A100 80GB / H100 80GB GPUs (tony-3 & hopper-1/2/3)
universe                = vanilla
initialdir              = /nethome/USERNAME/vllm_server
executable              = src/vllm_server/start_vllm/start_vllm_80gb.sh
output	                = /scratch/USERNAME/vllm_server/run.sh.$(ClusterId).$(Year)_$(Month)_$(Day)_$(SUBMIT_TIME).out
error                   = /scratch/USERNAME/vllm_server/run.sh.$(ClusterId).$(Year)_$(Month)_$(Day)_$(SUBMIT_TIME).err
log                     = /scratch/USERNAME/vllm_server/run.sh.$(ClusterId).$(Year)_$(Month)_$(Day)_$(SUBMIT_TIME).log
request_CPUs            = 16
request_memory          = 150G
request_GPUs            = 1
requirements            = (GPUs_GlobalMemoryMb >= 50000) && (TARGET.UidDomain == "coli.uni-saarland.de")

getenv                  = True
+WantGPUHomeMounted     = true

queue 1
"""

if __name__=="__main__":
    submit_file_dir = "submit_files/"
    username = input("Please enter your LST username (without the @lst.uni-saarland.de) : ")

    # writing customised submit files

    tiny_gpu = template_40gb.replace('USERNAME', username)
    big_gpu = template_80gb.replace('USERNAME', username)

    #creating log dir in /scratch
    os.makedirs(f"/scratch/{username}/vllm_server", exist_ok=True)
    
    tiny_sub = os.path.join("src/vllm_server/submit_files", f"{username}_submit_2x40gb.sub")
    big_sub = os.path.join("src/vllm_server/submit_files", f"{username}_submit_80gb.sub")

    with open(tiny_sub, "w") as f:
        f.write(tiny_gpu)
    with open(big_sub, "w") as f:
        f.write(big_gpu)

