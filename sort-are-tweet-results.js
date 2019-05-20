const results = require('./are-tweet-results.json');

let scoresByTweet = {};

// initialize at 0 positive, 0 negative per tweet
let tweets = Object.keys(results[0]);
tweets.forEach((tweet) => {
  scoresByTweet[tweet] = [0, 0];
});

// sum up across algorithms
results.forEach((algo) => {
  tweets.forEach((tweet) => {
    let pos = algo[tweet].positive,
        neg = algo[tweet].negative;
    scoresByTweet[tweet][0] += pos;
    scoresByTweet[tweet][1] += neg;
  });
});

// final averaging
tweets.forEach((tweet) => {
  let pos = scoresByTweet[tweet][0],
      neg = scoresByTweet[tweet][1];
  scoresByTweet[tweet].push(pos / (pos + neg));
  scoresByTweet[tweet].push(neg / (pos + neg));
});

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
