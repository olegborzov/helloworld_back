docker-compose -f docker-compose.test.yml run test_web 2>> dockerlog.txt
tests_result=$?
if [ $tests_result != 0 ]; then
  echo "bad tests results ${tests_result}"
  exit $tests_result
fi
