const scoresByTweet = require('./asa-tweet-results.json');
let tweets = Object.keys(scoresByTweet);

console.log('most positives');
tweets = tweets.sort((a, b) => {
  return scoresByTweet[b][0] - scoresByTweet[a][0];
});
console.log(tweets[0]);
console.log(tweets[1]);

console.log('most negatives');
tweets = tweets.sort((a, b) => {
  return scoresByTweet[b][1] - scoresByTweet[a][1];
});
console.log(tweets[0]);

console.log('best average');
let atweets = tweets.filter((x) => {
  return scoresByTweet[x][0] + scoresByTweet[x][1] >= 30;
}).sort((a, b) => {
  return scoresByTweet[b][2] - scoresByTweet[a][2];
});
console.log(atweets[0]);
console.log(atweets[1]);

console.log('worst average');
let btweets = tweets.filter((x) => {
  return scoresByTweet[x][0] + scoresByTweet[x][1] >= 30;
}).sort((a, b) => {
  return scoresByTweet[b][3] - scoresByTweet[a][3];
});
console.log(btweets[1]);
