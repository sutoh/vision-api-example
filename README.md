Google Cloud API Access Tools

# init

## この辺を参考に
https://developers.google.com/api-client-library/python/apis/vision/v1?hl=ja
https://cloud.google.com/vision/docs/label-tutorial?hl=ja

## アカウント情報
```
export GOOGLE_APPLICATION_CREDENTIALS=/Users/Shohei/project/hint/key/service-account.json
```

# Usage

```
$ gsutil cp IMG_xxxx.JPG gs://bucket-name/
$ python vision.py --help
$ python vision.py gs://bucket-name/IMG_xxxx.JPG --type label | jq
```


