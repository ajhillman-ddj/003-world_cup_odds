[![scheduled](https://github.com/ajhillman-ddj/003-world_cup_odds/actions/workflows/main.yml/badge.svg)](https://github.com/ajhillman-ddj/003-world_cup_odds/actions/workflows/main.yml)

# 003-world_cup_odds

This was a project to visualise the twists and turns of the World Cup. It was intended as an opportunity to practise set up scrapers using GitHub Actions and building applications in Svelte.

## Web scraping

I started by scraping outright winner odds from the Oddschecker website at regular intervals during each world cup game. This process was conducted using Selenium and GitHub Actions. The scraping code is contained in [this notebook.](https://github.com/ajhillman-ddj/003-world_cup_odds/blob/main/01-web_scraping_oddschecker_site.ipynb) The scheduling instructions were developed using [this code](https://github.com/ajhillman-ddj/003-world_cup_odds/blob/main/02-listing_scheduled_runs.ipynb) and are included in [this .yaml file.](https://github.com/ajhillman-ddj/003-world_cup_odds/blob/main/.github/workflows/main.yml)

Once I had the data, I built a Svelte app to visualise it. The app utilises a "discontinuous scale" to create more pixel space for in-game time:

```
$: xDomainArray = [$xDomain[0], new Date("2022-11-20 00:00:00.000")]

$: xRangeArray = [0, 0.1*graphWidth]

$: { 

xDomainArray = [$xDomain[0], new Date("2022-11-20 00:00:00.000")]
xRangeArray = [0, 0.1*graphWidth]

selectedGames.forEach((e,i) => {

let extraRange1 = ((new Date(e["StartDateTime"]) - xDomainArray[xDomainArray.length-1])/(totalDistance - totalSelectedGamesTime))*betweenGamesSpace
let extraRange2 = ((new Date(e["EndDateTime"]) - new Date(e["StartDateTime"]))/(totalSelectedGamesTime))*gameSpace

xDomainArray = [...xDomainArray,...[new Date(e["StartDateTime"]), new Date(e["EndDateTime"])]];
xRangeArray = [...xRangeArray,...[xRangeArray[xRangeArray.length-1]+extraRange1*graphWidth,xRangeArray[xRangeArray.length-1]+(extraRange1+extraRange2)*graphWidth]];

})

}

$: xRangeArray = xRangeArray.map(function(x) { return x*(view["index"] < 3 ? graphWidth : graphHeight)/1000; });

$: xScale = scaleLinear()
		.domain([...xDomainArray, $xDomain[1]])
		.range(view["index"] < 3 ? [...xRangeArray, graphWidth] : [...xRangeArray, graphHeight]);
```
