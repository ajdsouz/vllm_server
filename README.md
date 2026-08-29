# vLLM Server Installation and Init 

This repo installs vLLM (v0.16.0 x86-64, cuda 12.8) in the environment. To start, install [uv](https://astral.sh/uv). We will use uv as our package manager. 

## Installation

After uv installation is complete, run 

```bash
uv sync # <- run this at the root of the repo
```

This will create a virtual environment inside the project at `.venv/` and start installing the dependencies according to the `pyproject.toml` file. Once this is complete, you can verify everything is installed correctly by running ```uv pip list``` which will print out all installed packages.

## Starting vLLM server

For ease of use, I have created a script that will generate submit files from a template. Run `python make_submit_files.py` and you will be prompted to enter your LST username (without @lst.uni-saarland.de). After running the script, you will have two submit files, `USERNAME_submit_2x40gb.sub` and `USERNAME_submit_80gb.sub`. The former will use 2 40GB gpus on `tony-1/2/4` wile the latter will use 1 80GB gpu on any of the capable nodes (`tony-3, hopper-1/2/3`). We want to avoid using multiple GPUs on `tony-3` because nccl is broken preventing inter-gpu comms. Summarized,

1. Make submit files
    ```bash
    > python make_submit_files.py
    Please enter your LST username (without the @lst.uni-saarland.de) : mmusterman
    ```
2. Look at available GPUs on condor (on the submit node)
    ```bash
    condor_nodestate
    ```
3. Depending on the available node & GPUs, submit the corresponding submit file
    ```bash
    condor_submit src/vllm_server/submit_files/[username]_submit_2x40gb.sub -batch-name vllm-server
    ```
4. Find the job id 
    ```bash
    condor_q
    ```
5. Using `tail` on one of the ssh capable compute nodes (`jones-x`), check if the server has started. Model loading and server initialization will take around 5-10 minutes.
    ```bash
    tail -f /scratch/[username]/vllm_server/logs/[jobid]-[clusterid]-[date].out # you can just tab after entering jobid as path will be autocompleted 
    ```

6. Create a tunnel between your local device and the remote server

    a. Find the node the job is running on

    ```bash
    condor_q -run [jobid]
    ```

    b. Create tunnel between compute node to your device

    ```bash
    ssh -L 8000:EXECUTE_MACHINE:8000 [username]@login.lst.uni-saarland.de
    ```

    c. Test connection to node

    ```bash
    curl http://localhost:8000/v1
    ```