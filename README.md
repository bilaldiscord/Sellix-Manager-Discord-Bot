<div align="center">
  <img src="static/logo_with_text_teal.svg" width="400">

  Empty
  


</div>



## 📦 Download Python 3.10.0


- [🌎 Click here to download]((https://www.python.org/downloads/release/python-3100/))

### How to run the bot

Go to config.json and fill the following:

```sh
{
    "token": "",
    "sellix_api_key":  ""
}
```

Now go to your console and run the following command:

```sh
python main.py
```

### How to extend mock backend

When the mode is enabled, all API calls will be passed to `src/cloud/api/mock/mockHandler.ts`.

The source code is quite similar to a router interface. All you need to is `method`, `pathname` and a handler function. So, when you confront `Not Found` error while calling `GET /api/something`, you can simply add a mock route like below.

```ts
{
  method: 'get',
  pathname: 'api/something',
  handler: ({ search }): GetSomethingResponse => {
    return {
      ...something
    }
  },
}
```

### Scripts

- Packages
  - `pip install py-cord` : Run webpack for the cloud space
  - `pip install requests` : Run webpack for the desktop app main window renderer
  - `pip install discord` : Run webpack for the desktop app main processor
