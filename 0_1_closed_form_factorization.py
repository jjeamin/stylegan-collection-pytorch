import argparse

import torch


def main(args):
    ckpt = torch.load(args.ckpt)
    modulate = {
        k: v
        for k, v in ckpt["g_ema"].items()
        if "modulation" in k and "to_rgbs" not in k and "weight" in k
    }

    weight_mat = []
    for k, v in modulate.items():
        weight_mat.append(v)

    W = torch.cat(weight_mat, 0)
    eigvec = torch.svd(W).V.to("cpu")

    torch.save({"ckpt": args.ckpt, "eigvec": eigvec}, args.out)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Extract factor/eigenvectors of latent spaces using closed form factorization"
    )

    parser.add_argument(
        "--out", 
        type=str, 
        default='../checkpoint/factor.pt',
        help="name of the result factor file"
    )
    parser.add_argument(
        "--ckpt", 
        type=str, 
        default='../checkpoint/stylegan2-ffhq-config-f.pt',
        help="name of the model checkpoint")

    args = parser.parse_args()
    
    main(args)
