msg_text="helloworld #back #${HW_ENV} - $1"

curl -L -X POST "https://api.telegram.org/bot${HW_TG_BOT_TOKEN}/sendMessage?chat_id=${HW_TG_CHAT_ID}" \
  -H "Content-Type: application/json" --data-raw "{\"text\": \"${msg_text}\"}"
