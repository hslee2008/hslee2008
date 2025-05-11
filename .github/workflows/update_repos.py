import requests
import os

GH_TOKEN = os.getenv("GH_TOKEN")
GH_USERNAME = os.getenv("GH_USERNAME")

query = """
{
  user(login: "%s") {
    repositoriesContributedTo(first: 100, contributionTypes: [COMMIT, PULL_REQUEST], includeUserRepositories: false) {
      nodes {
        nameWithOwner
        url
        stargazerCount
      }
    }
  }
}
""" % GH_USERNAME

headers = {
    "Authorization": f"bearer {GH_TOKEN}"
}

res = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
repos = res.json()['data']['user']['repositoriesContributedTo']['nodes']

# Sort repos by stars
top_repos = sorted(repos, key=lambda r: r['stargazerCount'], reverse=True)[:5]

# Format as Markdown list
markdown_list = '\n'.join([f"- [{r['nameWithOwner']}]({r['url']}) ⭐ {r['stargazerCount']}" for r in top_repos])

# Replace section in README
with open("README.md", "r") as f:
    content = f.read()

start_tag = "<!--START_TOP_REPOS-->"
end_tag = "<!--END_TOP_REPOS-->"
new_section = f"{start_tag}\n{markdown_list}\n{end_tag}"

if start_tag in content and end_tag in content:
    content = content.split(start_tag)[0] + new_section + content.split(end_tag)[1]
else:
    content += f"\n\n{new_section}"

with open("README.md", "w") as f:
    f.write(content)