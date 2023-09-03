# Robust Change Captioning Repository

## Table of Contents
-[Documentation](#documentation)
- [Colab Setup](#colab-setup)
- [Data](#data)
- [Data Preprocessing](#data-preprocessing)
- [Training](#training)
- [Testing](#testing)
- [Evaluation](#evaluation)
- [Our Results](#our-results)

## Documentation
You Can find article about this repository [here](https://drive.google.com/file/d/1afR7gHOXX-Hs93__5WEB9LXaJcl3iy0U/view?usp=sharing)

## Colab Setup
1. You can access all project files [here](https://drive.google.com/drive/folders/1HgLErwlXiNE0L3IAc3_4CQH6HYizLUVR).
2. Follow these steps to run the project on Colab: [Colab Setup](https://colab.research.google.com/drive/1jPJVQsbgasoGfK3c_CIG3qY-XQuYN-tj?usp=sharing).
3. To run the project, especially for the extract_features, train, and test phases, you'll need at least a Tesla T4.

## Data
1. Download all data from [this link](https://drive.google.com/drive/folders/1KZ-wtfKwe6QiahSW99TxgNwgCNKDroMV?usp=sharing).

2. The downloaded data includes 9 folders:
   - `images` -> default images
   - `sc_images` -> semantically changed images
   - `nsc_images` -> distractor images
   - `features_resnet101` -> default images’ features extracted using ResNet-101
   - `sc_features_resnet101` -> semantically changed images’ features extracted using ResNet-101
   - `nsc_features_resnet101` -> distractor images’ features extracted using ResNet-101
   - `features_resnet50` -> default images’ features extracted using ResNet-50
   - `sc_features_resnet50` -> semantically changed images’ features extracted using ResNet-50
   - `nsc_features_resnet50` -> distractor images’ features extracted using ResNet-50

3. Data Preprocessing:
   - Extract visual features using ImageNet pretrained ResNet-101:
     ### Processing default images
     ```shell
     python scripts/extract_features.py --input_image_dir ./data/images --output_dir ./data/features --batch_size 128
     ```

     ### Processing semantically changed images
     ```shell
     python scripts/extract_features.py --input_image_dir ./data/sc_images --output_dir ./data/sc_features --batch_size 128
     ```

     ### Processing distractor images
     ```shell
     python scripts/extract_features.py --input_image_dir ./data/nsc_images --output_dir ./data/nsc_features --batch_size 128
     ```

   - Extract visual features using ImageNet pretrained ResNet-50:
     ### Processing default images
     ```shell
     python scripts/extract_features.py --input_image_dir ./data/images --output_dir ./data/features --batch_size 128 --model resnet50
     ```

     ### Processing semantically changed images
     ```shell
     python scripts/extract_features.py --input_image_dir ./data/sc_images --output_dir ./data/sc_features --batch_size 128 --model resnet50
     ```

     ### Processing distractor images
     ```shell
     python scripts/extract_features.py --input_image_dir ./data/nsc_images --output_dir ./data/nsc_features --batch_size 128 --model resnet50
     ```

4. Creating Vocabulary and Extracting Labels:
   Run the following code:
   ```shell
   python scripts/preprocess_captions.py --input_captions_json ./data/change_captions.json --input_neg_captions_json ./data/no_change_captions.json --input_image_dir ./data/images --split_json ./data/splits.json --output_vocab_json ./data/vocab.json --output_h5 ./data/labels.h5


## Training
To train the model, follow these steps:
1. Create a folder named 'experiments' to store all outputs:
```shell
mkdir experiments
```

2. Visualize Loss and Accuracy:
Start the visdom server to visualize loss and accuracy:
```shell
python -m visdom.server
```

3. Start Training:
Run the following code:
```shell
python train.py --cfg configs/dynamic/dynamic.yaml
```

4. Visualize Loss and Accuracy (Optional):
To visualize loss and accuracy, use the following command:
```shell
python train.py --cfg configs/dynamic/dynamic.yaml --visualize
```

5. Modify Dynamic Weights:
You can modify dynamic weights using the entropy_weight parameter:
```shell
python train.py --cfg configs/dynamic/dynamic.yaml --visualize --entropy_weight 0.0001
```

## Testing

To test a model with a specific snapshot, use the following code:

```shell
python test.py --cfg configs/dynamic/dynamic.yaml --visualize --snapshot 9000 --gpu 1
```
This code tests the model at snapshot 9000. If the --snapshot argument is not provided, the model is tested with the latest snapshot.

## Evaluation

### Caption Evaluation

After formatting the results, run the following code for caption evaluation:
```shell
python utils/eval_utils.py
```
### Viewing Evaluation Results
The results will be displayed in this folder: ./experiments/dynamic/eval_sents/eval_results.txt

## Our Results
You can access all results in the [Google Drive link](https://drive.google.com/drive/folders/1HgLErwlXiNE0L3IAc3_4CQH6HYizLUVR). All results are named with the following format: 'experiments_numberOfExperiment_resnetType_batchSize_batchSizeNumber,' for example: `experiments_7_resnet50_batchSize_32` represents the results of the 7th experiment, where features were extracted with ResNet-50 and a batch size of 32 was used.


