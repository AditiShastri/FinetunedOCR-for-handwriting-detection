CUDA_VISIBLE_DEVICES=0 python tools/predict.py --model_path model_best.pth --input_folder ./input --output_folder ./output --thre 0.7 --polygon --show --save_result
