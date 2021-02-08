###参考サイト

loggingの概要については公式サイトおよび以下のエントリが参考になります。

・Python 公式 Logging HOWTO
https://docs.python.jp/3/howto/logging.html#logging-flow

・Django 公式 ロギング
https://docs.djangoproject.com/ja/2.0/topics/logging/

・logging入門
https://qiita.com/knknkn1162/items/87b1153c212b27bd52b4

##loggingのしくみ

細かく書くときりがないので、Djangoで必要な最低限の内容だけまとめます。

###loggingの構成要素

loggingはLoggers、Handlers、Filters、Formattersの４つの要素で構成されます。

- Logger
 - ログ出力を受け付ける。
- Handler
 - ログの出力先を設定する（標準出力、ファイル、メール等）
- Filter
 - ログレベルとは別にブール型関数でフィルタを設定する
- Formatter
 - ログに出力する文字列の形式を設定する

FilterとFormatterはHandlerの属性、HandlerはLoggerの属性です。
Loggerでは複数のHandlerを指定することができます。

### ログレベル

loggingでは個々のログのことをログレコードと呼びます。
ログレコードは重要度に応じた７段階のログレベルがあります。

|名前|設定値|役割 
|:--|:--|:--|
|NOTSET|0|設定値などの記録（全ての記録）|
|DEBUG|10|動作確認などデバッグの記録|
|INFO|20|正常動作の記録
|WARNING|30|警告の記録
|ERROR|40|エラーなど重大な問題
|CRITICAL|50|停止など致命的な問題

コード内で任意のロガーを指定し、ログレベルと同名のメソッドを実行するとログが出力されます。

例；

```py
import logging
…
logger = logging.getLogger('development')
logger.info('Hello World!')
```

ログレベルはLogger及びHandlerのlevel属性で利用されます。level属性に任意のログレベルを指定すると、そのレベル未満の出力を抑制できます。

### Logger の名前空間

Loggerの名前はドット区切りにして名前空間を持つことができます。
名前空間を作ると、getLoggerによるLoggerの指定で該当のLoggerが無かった場合、上位のLoggerの取得を試みます。具体的には、getLogger('first.second.third')とすると、first.second.thirdロガーが無い場合、first.second ロガー、first ロガー、ルートロガーの順に取得を試みます（名前が空文字のLoggerを作るとルートLoggerとなります）。

Loggersの定義はルートに近い上位のものから順に定義します。Loggerのpropagate属性をTrueにすると、該当Loggerでの処理後に再帰的に次のLoggerを取得します。

この動作を前提として、Loggerの取得は以下のように記述するように推奨されています。

```py
logging.getLogger(__name__)
```

pythonにより「\_\_name__」にはモジュール名が代入されるので、モジュールのディレクトリ構造にあわせて出力内容を変更できます。

## デフォルト設定

「django.utils.log.py」の`DEFAULT_LOGGING`がDjangoのloggingのデフォルト設定です。最初はこの設定をsetting.pyに`LOGGING`としてコピーして、修正を加えて動作を確認してみるのがよいと思います。

```py:django.utils.log.py
# Default logging for Django. This sends an email to the site admins on every
# HTTP 500 error. Depending on DEBUG, all other log records are either sent to
# the console (DEBUG=True) or discarded (DEBUG=False) by means of the
# require_debug_true filter.
DEFAULT_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'django.server': {
            '()': 'django.utils.log.ServerFormatter',
            'format': '[%(server_time)s] %(message)s a',
        }
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        },
        'django.server': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'django.server',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'mail_admins'],
            'level': 'INFO',
        },
        'django.server': {
            'handlers': ['django.server'],
            'level': 'INFO',
            'propagate': False,
        },
    }
}
```
### デフォルト設定の説明

・loggers

djangoとdjango.serverというLoggerが用意されています。djangoは内部処理全般、django.serverは開発用Webサーバのアクセスログの出力です。

・handlers ： 出力先のhandlers

デバッグ時は標準出力、本番運用時はERROR以上を管理者にメールする設定です。「500 Internal Server Error」の発生時に毎回メールが送信されます（SMTP及び管理者のメールアドレスが設定されている場合）。

・filters 

DEBUG設定 の ON/OFFを使ったフィルターが用意されています。
  
### 自分のアプリケーション用のLoggerを追加する方法

デフォルトのLoggersには自分のアプリケーション内でデバッグログを出力する設定がありません。専用の設定を追加することでログ出力が可能になります。

サンプル

```py:settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'django.server': {
            '()': 'django.utils.log.ServerFormatter',
            'format': '[%(server_time)s] %(message)s a',
        },
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '%(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'django.server': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'django.server',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'mail_admins'],
            'level': 'INFO',
        },
        'django.server': {
            'handlers': ['django.server'],
            'level': 'INFO',
            'propagate': False,
        },
        #追加
        'myapp': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    }
}
```

##本番環境用設定についての考察

・デフォルトの設定はDEBUGフラグで開発・本番の切り替えを行っているが、そもそも別のファイルにするのが主流かつ安全。

・クラウド環境で運用する場合、アプリケーションのログ出力は標準出力だけ限定し、ファイル出力やログ監視は別のサービスで行うことが推奨されている。[Twelve-Factor App ： ログをイベントストリームとして扱う](https://12factor.net/ja/logs)を参照。

・エラー集計サービスにエラーログを直接送信する方法もある。代表的なものが「sentry」でありDjangoのクライアントパッケージもある。設定方法についてはcookiecutter-djangoが参考になる。