# Robust Change Captioning Reposunun içeriği aşağıdaki makale için kod ve veri içermektedir:

## Colab İçin Gerekli Adımlar
1. Buradan tüm projenin dosyalarına erişilebilir: https://drive.google.com/drive/folders/1HgLErwlXiNE0L3IAc3_4CQH6HYizLUVR
2. Buradan da projenin çalıştırılması için gerekli adımlar sırasıyla verilmiştir:https://colab.research.google.com/drive/1jPJVQsbgasoGfK3c_CIG3qY-XQuYN-tj?usp=sharing
3. Projeyi ayağa kaldırmak ve özellikle extract_features, train ve test aşamaları için en az Tesla T4 gereklidir.

## Data
1. Buradan tüm Data’yı indirebilirsiniz: https://drive.google.com/drive/folders/1KZ-wtfKwe6QiahSW99TxgNwgCNKDroMV?usp=sharing

2. İndirdiğiniz data içerisinde 9 adet klasör bulunmaktadır. Bunlar;
– images –> default images
– sc_images –> semantically changed images
– nsc_images –> distractor images
– features_resnet101 –> default images’ features extracted using ResNet-101
– sc_features_resnet101 –> semantically changed images’ features extracted using ResNet-101
– nsc_features_resnet101 –> distractor images’ features extracted using ResNet-101
– features_resnet50 –> default images’ features extracted using ResNet-50
– sc_features_resnet50 –> semantically changed images’ features extracted using ResNet-50
– nsc_features_resnet50 –> distractor images’ features extracted using ResNet-50

3. Preprocess The data
Preprocess işlemlerinin tamamını yukarıdaki Data linki üzerinden bulabilirsiniz. Ya da ayrıca kendiniz preprocess işlemlerini yapabilirsiniz.
• Extract visual features using ImageNet pretrained ResNet-101:
# processing default images
python scripts/extract_features.py --input_image_dir ./data/images --output_dir ./data/features --batch_size 128

# processing semantically changes images
python scripts/extract_features.py --input_image_dir ./data/sc_images --output_dir ./data/sc_features --batch_size 128

# processing distractor images
python scripts/extract_features.py --input_image_dir ./data/nsc_images --output_dir ./data/nsc_features --batch_size 128
• Extract visual features using ImageNet pretrained ResNet-50:
# processing default images
python scripts/extract_features.py --input_image_dir ./data/images --output_dir ./data/features --batch_size 128 --model resnet50

# processing semantically changes images
python scripts/extract_features.py --input_image_dir ./data/sc_images --output_dir ./data/sc_features --batch_size 128 --model resnet50

# processing distractor images
python scripts/extract_features.py --input_image_dir ./data/nsc_images --output_dir ./data/nsc_features --batch_size 128 --model resnet50
• Vocab oluşturulamsı ve label’ların çıkarılması için aşağıdaki kodlar çalıştırılmalıdır:
python scripts/preprocess_captions.py --input_captions_json ./data/change_captions.json --input_neg_captions_json ./data/no_change_captions.json --input_image_dir ./data/images --split_json ./data/splits.json --output_vocab_json ./data/vocab.json --output_h5 ./data/labels.h5

Train İşlemi
Modeli eğitmek için aşağıdaki adımlar yapılmalıdır:
# experiments isminde Tüm çıktıları tutmak için klasör oluşturun.
mkdir experiments

# Tüm loss ve accuracy değerlerini görselleştirmek için visdom server'ı başlatın.
python -m visdom.server

# Traini Başlatmak için aşağıdaki kodu çalıştırın.
python train.py --cfg configs/dynamic/dynamic.yaml 
Tüm loss ve accuracy değerlerini görselleştirmek için visdom server’ı başlatın.
python train.py --cfg configs/dynamic/dynamic.yaml --visualize
entropy_weight değerini kullanarak dinamik ağırlıkları değiştirilebilir.
python train.py --cfg configs/dynamic/dynamic.yaml --visualize --entropy_weight 0.0001

Test İşlemi
Belirli snapshot’u alınmış modeli test etmek için aşağıdaki kodu çalıştırın.
python test.py --cfg configs/dynamic/dynamic.yaml --visualize --snapshot 9000 --gpu 1
Bu kod, modeli 9000. snapshot’ta test eder. Eğer –snapshot argümanı verilmezse, model en son snapshot’ta test edilir.

Evaluation
• Caption evaluation
python utils/eval_utils.py
Format hazırlandıktan sonra aşağıdaki kod çalıştırılmalıdır:
# This will run evaluation on the results generated from the validation set and print the best results
python evaluate.py --results_dir ./experiments/dynamic/eval_sents --anno ./data/total_change_captions_reformat.json --type_file ./data/type_mapping.json
Sonuç bu klasörde gösterilmektedir: ./experiments/dynamic/eval_sents/eval_results.txt

Bizim Sonuçlarımız
Yukarıda verilmiş tüm projenin drive linki olan https://drive.google.com/drive/folders/1HgLErwlXiNE0L3IAc3_4CQH6HYizLUVR) linkten tüm sonuçlara erişilebilir. Tüm sonuçların isim kodlaması şu şekildedir: ‘experiments_numberOfExperiment_resnetType_batchSize_batchSizeNumber’ örneğin: experiments_7_resnet50_batchSize_32 –> 7. deneyin sonuçlarıdır. ResNet-50 ile özellikleri çıkarılmış ve batch size 32 ile eğitilmiştir.
