docker-compose -f docker-compose.test.yml run --rm test_web 2>> dockerlog.txt
tests_result=$?
docker-compose -f docker-compose.test.yml down --remove-orphans --rmi all
docker-compose down --remove-orphans --rmi all
if [ $tests_result != 0 ]; then
  exit $tests_result
fi
