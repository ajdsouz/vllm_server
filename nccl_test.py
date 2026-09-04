import os
import torch
import torch.distributed as dist

rank = int(os.environ["RANK"])
local_rank = int(os.environ["LOCAL_RANK"])

torch.cuda.set_device(local_rank)

print(f"rank={rank}, local_rank={local_rank}, GPU={torch.cuda.get_device_name()}")

dist.init_process_group(
    backend="nccl",
    init_method="env://",
    world_size=2,
    rank=rank,
)

print(f"rank={rank}: NCCL process group initialized")

x = torch.ones(128, device="cuda") * (rank + 1)

print(f"rank={rank}: before all_reduce")
dist.all_reduce(x)
print(f"rank={rank}: after all_reduce, value={x[0].item()}")

dist.barrier()

if rank == 0:
    print("SUCCESS: NCCL communication works")

dist.destroy_process_group()
