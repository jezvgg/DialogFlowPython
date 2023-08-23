# DialogFlowPython
###### Examples of use DialogFlow with Python

###### На данном репозиторие вы можете посмотреть примеры использования DialogFlow на Python, создание с его помощью телеграм бота и другое.

## Установка gcloud CLI

Для работы с DialogFlow на python вам первым делом нужно зарегестрироваться на DialogFlow и сделать своего агента.
---> https://dialogflow.cloud.google.com/
 ссылка на обзор работы с DialogFlow: https://vc.ru/services/71166-poshagovaya-instrukciya-po-sozdaniyu-chat-bota-na-dialogflow-bez-znaniy-programmirovaniya

 Потом вам нужно подключить к вашему комьютеру Google Cloud SDK.
 **ссылка:** https://cloud.google.com/sdk/docs/install

 1. Если вы на **Windows**:
    1. Установите https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe
        Либо запустите следущее в shell:
        ```shell
        (New-Object Net.WebClient).DownloadFile("https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe", "$env:Temp\GoogleCloudSDKInstaller.exe")

        & $env:Temp\GoogleCloudSDKInstaller.exe
    
        ```
    2. Запустите установщик

2. Если вы на **Linux**
    1. Выполните команду
        ```
        curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-436.0.0-linux-x86_64.tar.gz
        ```
    2. Потом вот эту:
        ```
        tar -xf google-cloud-cli-436.0.0-linux-x86.tar.gz
        ```
    3. Вот эту:
        ```
        ./google-cloud-sdk/install.sh
        ```
    4. Откройте новый терминал, чтоб измнения вошли в силу и введите следующую команду для инициализации gcloud CLI и войдите в свой аккаунт.
        ```
        ./google-cloud-sdk/bin/gcloud init
        ```

Если что-то не получилось установите то переходите по ссылке, которая была дана выше, там всё подробно описано.

### Регистрация агента

Для регистрации агента введите эту команду в консоль:
```
gcloud auth application-default login
```
Вам нужно будет зарегестрировать аккаунт и выбрать ваш проект. ( Где его можно найти ищите ниже, где project_id )
Возможно, вам после установки СДК автоматичеси предложит зарегестрировать агента. Тогда у вас напишет, что уже зарегестрировано.

! ВАЖНО ! gcloud работает с Python от версии 3.5 до версии 3.9. Перепроверьте, что у вас подходящая версия для работы с ним.

### Установка нужной библеотеки

Перейдём к работе с DialogFlow на Python.
Для работы с ним вам понадобиться установить библеотеку google
Для этого воспользуйтесь pip:
```
pip install google-cloud-dialogflow
```
( в коде импортируется from google.cloud import dialogflow )

### ID, Token и прочее для работы

И для работы с программами вам нужны ещё несколько вещей:
1. project_id
2. session_id
3. language

**project_id** - id вашего проекта, так, как мы работаем с DialogFlow, то заходим туда, тыкаем на шестерёнку слева сверху и заходим в настройки.
Во вкладке General мы должны найти project_id - это то, что мы ищем.
[![Демонстрационая вкладка](https://imgur.com/a/4BGmX5W "Демонстрационая вкладка")](https://imgur.com/a/4BGmX5W "Демонстрационая вкладка")

**session_id** - id сессии, в документации gcloud dialogflow сказано, что может быть любым. Для тестирования часто используют *123456789*

**language** - язык работы бота, писать с маленькой буквы, например *ru*
