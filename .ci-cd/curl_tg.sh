# Пример вызова скрипта
# sh .ci-cd/curl_tg.sh "110201543:AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw" "-1001234567890" dev "test"

HW_TG_BOT_TOKEN=$1     # Токен бота Telegram (пример - 110201543:AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw)
HW_TG_CHAT_ID=$2       # ID чата/канала в Telegram, куда бот будет отправлять сообщения (пример -1001234567890)
HW_ENV=$3              # Окружение (dev/prod)
HW_MESSAGE=$4          # Сообщение

msg_text="helloworld #back #${HW_ENV} - ${HW_MESSAGE}"

curl -L -X POST "https://api.telegram.org/bot${HW_TG_BOT_TOKEN}/sendMessage?chat_id=${HW_TG_CHAT_ID}" \
  -H "Content-Type: application/json" --data-raw "{\"text\": \"${msg_text}\"}"
