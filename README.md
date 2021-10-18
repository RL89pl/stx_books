STX BOOKS

Add/Update data set from https://www.googleapis.com/books/v1/volumes?q=war:

```python
data = {
    "q": "war"
}
r = requests.post("http://stx.otar.usermd.net/db", data=data).json()
```
