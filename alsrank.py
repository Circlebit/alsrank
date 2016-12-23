# this script performs a google search for given items
# and checks on how  many werbeartikel-schenken.de domains
# are in the results

import google
import terminaltables as tt


def get_urls(query, n=10):
    # returns a list of n URLs from google search with a given query
    result = []
    search = google.search(query, tld='de', lang='de')
    for i in range(n):
        result.append(next(search))
    return result


def find_url(urls, target):
    # takes a list of urls
    # returns a list of lists [url containing target, index of url]
    result = []
    rank = 1
    for e in urls:
        if target in e:
            result.append([rank, e])
        rank += 1
    return result


def combine_queries(items, pre=[], post=[]):
    # takes three lists and returns a list of combinations
    result = [] + items
    for item in items:
        for e in pre:
            result.append(e + " " + item)
        for e in post:
            result.append(item + " " + e)
    return result


def check_queries(queries, target="werbeartikel-schenken.de", depth=10):
    # check a list of google queries for appearance of target
    result = []
    all_urls = []
    url_index = []
    for q in queries:
        all_urls = get_urls(q, depth)
        url_index.append([q, all_urls])
    for l in url_index:
        result.append([l[0], find_url(l[1], target)])
    return result


def pr_table(rawdata):
    # takes data as given back by check_queries() and prints pretty table
    nofind = []
    tabledata = [["Suchbegriff", "w-s.de Treffer"]]

    for target in rawdata:
        if not target[1]:    # if there are no urls in this targets list:
            nofind.append(target[0])  # append it to the nofind list
        else:                # if there's something in there:
            urlstr = ""
            for url in target[1]:  # append all those URLs to a formated string
                urlstr += str(url[0]) + ". " + url[1] + "\n"
            tabledata.append([target[0], urlstr])  # add the string to a list

    # printing the table with terminaltables
    table = tt.AsciiTable(tabledata)
    print(table.table)
    print("\nkeine Treffer für: ")
    print(*nofind, sep=', ')


# Suchbegriffe #
items = ['Wassereis', 'Eis']
pre = ['bedrucktes']
post = ['mit Werbedruck', 'mit Logo', 'bedrucken']

# Los geht's! #
queries = combine_queries(items, pre, post)  # make list of queries
data = check_queries(queries, depth=10)  # get results from google
pr_table(data)  # print nice table
