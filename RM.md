## 列、選択肢について

- 選択肢が一つも選ばれていなかった場合、その列は削除
    - 問14, 問21-3など
- 列はGoogleFormの順番
- 新たに作成した列の順番は選択肢が選ばれた順

## モジュールについて

- multiple_selection：　「その他」の選択肢が含まれないものの変換
- multiple_selection_other：　「その他」の選択肢が含まれるものの変換
- 複数選択不可の問についても変換可能

```python
import numpy as np
import pandas as pd

class MultipleSelection():
    def multiple_selection_other(self, df_raw, column_number, number_of_options, question_number):
        """「その他」あり

				引数
				-----
				df_raw: データフレームの名前
				column_number: df_raw.headで表示したデータのヘッダー番号
				number_of_options: 選択肢の数（その他も含む）
				question_number:　問番号（数字であればどのようなものでもOK)
				
				"""

				df = df_raw[column_number]

        df = pd.DataFrame(df)
        df[0] = df[column_number].str.split(',')
              # 0 is column name

        for i in range(number_of_options):
            df[i + 1] = 0

        df[0][1:] = df[0][1:].map(self.strip_space)

        ls_elm = []
        for index in df.iloc[1:, 1]:
            try:
                for elm in index:
                    if elm not in ls_elm:
                        ls_elm.append(elm)
            except:
                pass
        ls_elm.insert(0, '')

        for index in range(df.shape[0]):
            try:
                for elm in df.iloc[index + 1, 1]:
                    num_elm = ls_elm.index(elm)
                    if num_elm >= number_of_options:
                        df.iloc[index + 1, number_of_options + 1] += 1
                    else:
                        df.iloc[index + 1, num_elm + 1] += 1
            except:
                pass

        ls_elm[0] = 0

        for _ in range(number_of_options, len(ls_elm)):
            ls_elm.pop(number_of_options)

        ls_elm.insert(number_of_options, 'その他')
        ls_elm.insert(0, question_number)

        df.columns = ls_elm

        df = df.drop(0, axis=1)

        return df

  def multiple_selection(self, df_raw, column_number, number_of_options, question_number):
        """「その他」なし

				引数
				-----
				df_raw: データフレームの名前
				column_number: df_raw.headで表示したデータのヘッダー番号
				number_of_options: 選択肢の数
				question_number:　問番号（数字であればどのようなものでもOK)
				
				"""      
				df = df_raw[column_number]

        df = pd.DataFrame(df)
        df[0] = df[column_number].str.split(',')

        for i in range(number_of_options):
            df[i + 1] = 0

        df[0][1:] = df[0][1:].map(self.strip_space)

        ls_elm = []
        for index in df.iloc[1:, 1]:
            try:
                for elm in index:
                    if elm not in ls_elm:
                        ls_elm.append(elm)
            except:
                pass
        ls_elm.insert(0, '')

        for index in range(df.shape[0]):
            try:
                for elm in df.iloc[index + 1, 1]:
                    num_elm = ls_elm.index(elm)
                    df.iloc[index + 1, num_elm + 1] += 1
            except:
                pass

        ls_elm[0] = 0

        ls_elm.insert(0, question_number)

        df.columns = ls_elm

        df = df.drop(0, axis=1)

        return df

    def strip_space(self, ls):
        ls_modified = []
        try:
            for elment in ls:
                elm_modified = elment.strip()
                ls_modified.append(elm_modified)
            return ls_modified
        except:
            pass
```

## 実行方法

### モジュールインポート

```python
import pandas as pd

from multiple_selection import MultipleSelection
```

### データの読み込みと表示

```python
df_raw = pd.read_csv('pre-enrollement-education.csv', header=None)
pd.set_option('display.max_columns', None)
df_raw.head(1)
```

### インスタンス化

```python
ms = MultipleSelection()
```

### 実行

```python
# ls_indexは行番号リスト0から始める
# ls_index = [0, 1, 2, 3, 4, ・・・ , n]
ls_index = [0, 1, 2, ・・・, 255]
df = df_raw.reindex(index=ls_index) # 行番号を振り直す
df_q6 = ms.multiple_selection_other(df, 6, 4, 16) # 行番号を振り直したものデータフレームとして入れる
ls_index = [0, 1, 2, ・・・, 255]
df_q6 = df_q6.reindex(index=ls_index)
df_q6
```

- ls_indexについて
    - 処理後の列名は選択肢として選ばれた順番で作成される
    - そのため正規の選択肢より先に違うものが現れた場合それが列名になる
    - 1つ目のls_indexを使って調整することで対応
    - 具体例　問6
        - 146(spreadsheet上では147)番目まで「学生」は出てこない
            - 今回の場合spredsheetでの行番号マイナス1
        - 146と11を入れ替える
            
            ```python
            ls_index = [0, 1, ・・・, 10, 146, 12, ・・・, 145, 11, 147, ・・・, 255]
            ```
            
    - 2つ目のls_indexでもとに戻す

### 選択肢の名称を一行下げる

```python
for i in range(1, df_q6.shape[1]):
    df_q6.iloc[0, i] = df_q6.columns[i]
```

### 結合

- 処理が要らないデータに関してはそのまま

```python
df_0to6 = df_raw.iloc[:, 0:6]
```

- 結合

```python
df_concat = df_0to6
df_concat = pd.concat([df_concat, df_q6], axis=1)
```

### csvに変換

```python
df_concat.to_csv('data_modified.csv', header=False, index=False)
```