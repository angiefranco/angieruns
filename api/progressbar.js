fetch('https://hope.drugfree.org/endurance-teams/angieruns');
//console.log('hi');
//curl https://hope.drugfree.org/endurance-teams/angieruns | grep -E '<span class="was-raised"' | grep -E -o "\d+" | head -1

const string = "<span class=\"was-raised\">\$450</span>"
const regex1 = new RegExp(' | grep -E \'<span class="was-raised\"\'');
const regex2 = new RegExp(' | grep -E -o "\d+"');
const regex3 = new RegExp(' | head -1');

result=string.concat(regex1);
result=result.concat(regex2);
result=result.concat(regex3);
console.log(result);