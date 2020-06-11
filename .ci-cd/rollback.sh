# 1. Устанавливаем из входных параметров переменные окружения
export HW_ENV=$1
export HW_TG_BOT_TOKEN=$2
export HW_TG_CHAT_ID=$3
printf "\n\n### %s - start_rollback###\n" "$(date)" >> dockerlog.txt

# 2. Откат деплоя на предыдущую версию
sh ./.ci-cd/curl_tg.sh "#start_rollback"

docker tag "hw_back_${HW_ENV}:latest" "hw_back_${HW_ENV}:temp"
docker tag "hw_back_${HW_ENV}:previous" "hw_back_${HW_ENV}:latest"
docker tag "hw_back_${HW_ENV}:temp" "hw_back_${HW_ENV}:previous"
docker-compose up -d

sh ./.ci-cd/curl_tg.sh "#end_rollback"
