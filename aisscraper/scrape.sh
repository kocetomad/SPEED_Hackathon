function fetch() {
        echo "Fetching x:$CURX y:$CURY"
        curl "https://www.marinetraffic.com/getData/get_data_json_4/z:13/X:$CURX/Y:$CURY/station:0" \
          -H 'authority: www.marinetraffic.com' \
          -H 'pragma: no-cache' \
          -H 'cache-control: no-cache' \
          -H 'accept: */*' \
          -H 'x-requested-with: XMLHttpRequest' \
          -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36' \
          -H 'vessel-image: 008c7c9e786b2fd0993d8a4530acbf434930' \
          -H 'sec-fetch-site: same-origin' \
          -H 'sec-fetch-mode: cors' \
          -H 'sec-fetch-dest: empty' \
          -H 'referer: https://www.marinetraffic.com/en/ais/home/centerx:-2.407/centery:50.572/zoom:13' \
          -H 'accept-language: en-GB,en;q=0.9,en-US;q=0.8' \
          -H 'cookie: __cfduid=d1ed2ac7090eb62fdf1c23c62291ca01f1594045278; SERVERID=app9; _ga=GA1.2.1219123965.1594045279; _gid=GA1.2.2100679767.1594045279; _hjid=e6508766-3f7c-439b-9aad-fb5f86e5a64f; vTo=1; _lfa=eyJZRWdrQjhsNkFLVzRlcDNaIjoiTEYxLjEuNDcxZTE1NTNkZjFmZDVlYS4xNTk0MDQ1Mjk1OTkzIn0%3D; __atuvc=3%7C28; _hjAbsoluteSessionInProgress=1; _gat=1; mp_017900c581ab83839036748f85e0877f_mixpanel=%7B%22distinct_id%22%3A%20%221732480abe5124-0b1d43d37cbe39-31617402-280000-1732480abe6d57%22%2C%22%24device_id%22%3A%20%221732480abe5124-0b1d43d37cbe39-31617402-280000-1732480abe6d57%22%2C%22%24search_engine%22%3A%20%22google%22%2C%22%24initial_referrer%22%3A%20%22https%3A%2F%2Fwww.google.com%2F%22%2C%22%24initial_referring_domain%22%3A%20%22www.google.com%22%7D' \
          --compressed --output ${DIR}/ais_${CURX}_${CURY}_${DATE}.json -s
}

DATE=`date +%F_%H_%M`
DIR=/home/ec2-user/ais/${DATE}
mkdir -p $DIR

CURX=2021
CURY=1378
fetch
CURX=2020
CURY=1378
fetch
CURX=2019
CURY=1378
fetch
CURX=2021
CURY=1379
fetch
CURX=2020
CURY=1379
fetch
CURX=2019
CURY=1379
fetch


cd $DIR
jq '.data.rows' * | jq -s add > all.json
jq 'unique_by(.SHIPNAME)' all.json > deduped.json

curl -X POST -o /dev/null -H "Content-Type: application/json" https://d0042529.daizy.io/aisdata --data @deduped.json
