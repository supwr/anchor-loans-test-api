Wedding Gallery API


##### Executing docker container for development

```
docker run -it -p 8000:5000 -v ~/Documentos/test-anchor-loans/wedding-gallery:/wedding-gallery --network=testanchorloans_anchor-loans_net --link anchor-loans-mongo testanchorloans_anchor-loans-site python3 /wedding-gallery/app/main.py
```