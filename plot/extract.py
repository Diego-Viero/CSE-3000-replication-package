import os
import sys
import pandas as pd
import matplotlib.pyplot as plt

iterations = 10
presets = 3
seconds = 60
series_type_name = 'total-time'

def quantize(data: pd.DataFrame):
    index = 0
    new_data = []
    np_data = data.values
    for i in range(seconds):
        if index == len(data) - 1:
            new_data.append([*np_data[index]])
            new_data[-1][5] = i
            continue

        while np_data[index][5] < i:
            index += 1
            if index == len(data) - 1:
                break
        
        new_data.append([*np_data[index]])
        new_data[-1][5] = i
    return pd.DataFrame(new_data, columns=data.columns)

def average(df: pd.DataFrame):
    averaged_data = []
    for namespace in df['namespace'].unique():
        df_1 = df[df['namespace'] == namespace]
        for preset in df_1['preset'].unique():
            df_2 = df_1[df_1['preset'] == preset]
            for i in range(seconds):
                df_3 = df_2[df_2['index'] == i].values
                averaged_data.append([*df_3[0]])
                averaged_data[-1][5] = df_3[:,5].mean()

    return pd.DataFrame(averaged_data, columns=df.columns)

def plot(df: pd.DataFrame):
    for namespace in df['namespace'].unique():
        df_1 = df[df['namespace'] == namespace]
        for preset in sorted(df_1['preset'].unique()):
            df_2 = df_1[df_1['preset'] == preset]
            plt.plot(df_2['index'], df_2['value'], label=preset)
        plt.title(namespace)
        plt.legend()
        plt.ylim(bottom=-1)
        plt.show()

def main(directory: str):
    big_data = []

    for folder in os.listdir(directory):
        if folder == 'properties.csv': 
            continue

        folders = os.listdir(f"{directory}/{folder}")
        if len(folders) == 0:
            print('missing fid folder in', folder)
            continue
        fid = folders[1] if 'FID-' in folders[1] else folders[0]

        if not os.path.exists(f'{directory}/{folder}/{fid}/metrics/properties.csv'):
            split = folder.split('-')
            print('missing properties.csv in folder:', folder, 'target file:', get_name(int(split[2])))
            continue

        properties_df = pd.read_csv(f'{directory}/{folder}/{fid}/metrics/properties.csv')
        namespace = properties_df.at[0, 'namespace']
        # if namespace != 'help.js':
        #     continue
        preset = properties_df.at[0, 'preset']
        series_df = pd.read_csv(f'{directory}/{folder}/{fid}/metrics/series.csv')
        series_df['preset'] = preset
        series_df = series_df[series_df['seriesTypeName'] == series_type_name] # only care about search time
        series_df = series_df[series_df['seriesName'] == 'branch-objectives-covered'] # only care about branches
        series_df = series_df.reset_index()
        series_df = quantize(series_df)
        big_data.extend(series_df.values)

    big_df = pd.DataFrame(big_data)
    big_df.columns = series_df.columns
    big_df = average(big_df)
    plot(big_df)
    
def get_name(index_to_look_for: int):
    projects = {
        "./benchmark/commanderjs": [
            "./benchmark/commanderjs/lib/help.js",
            "./benchmark/commanderjs/lib/option.js",
            "./benchmark/commanderjs/lib/suggestSimilar.js"
            ],
        "./benchmark/express": [
            # "./benchmark/express/lib/application.js",
            "./benchmark/express/lib/middleware/query.js",
            "./benchmark/express/lib/request.js",
            "./benchmark/express/lib/response.js",
            "./benchmark/express/lib/utils.js",
            "./benchmark/express/lib/view.js"
            ],
        "./benchmark/javascript-algorithms": [
            "./benchmark/javascript-algorithms/src/algorithms/graph/articulation-points/articulationPoints.js",
            "./benchmark/javascript-algorithms/src/algorithms/graph/bellman-ford/bellmanFord.js",
            "./benchmark/javascript-algorithms/src/algorithms/graph/travelling-salesman/bfTravellingSalesman.js",
            "./benchmark/javascript-algorithms/src/algorithms/graph/breadth-first-search/breadthFirstSearch.js",
            "./benchmark/javascript-algorithms/src/algorithms/graph/depth-first-search/depthFirstSearch.js",
            "./benchmark/javascript-algorithms/src/algorithms/graph/detect-cycle/detectDirectedCycle.js",
            "./benchmark/javascript-algorithms/src/algorithms/graph/detect-cycle/detectUndirectedCycle.js",
            # "./benchmark/javascript-algorithms/src/algorithms/graph/dijkstra/dijktra.js",
            "./benchmark/javascript-algorithms/src/algorithms/graph/eulerian-path/eulerianPath.js",
            "./benchmark/javascript-algorithms/src/algorithms/graph/floyd-warshall/floydWarshall.js",
            "./benchmark/javascript-algorithms/src/algorithms/graph/hamiltonian-cycle/hamiltonianCycle.js",
            "./benchmark/javascript-algorithms/src/algorithms/graph/kruskal/kruskal.js",
            "./benchmark/javascript-algorithms/src/algorithms/graph/prim/prim.js",
            "./benchmark/javascript-algorithms/src/algorithms/graph/strongly-connected-components/stronglyConnectedComponents.js",
            "./benchmark/javascript-algorithms/src/algorithms/sets/knapsack-problem/Knapsack.js",
            "./benchmark/javascript-algorithms/src/algorithms/sets/knapsack-problem/KnapsackItem.js",
            "./benchmark/javascript-algorithms/src/algorithms/math/matrix/Matrix.js",
            "./benchmark/javascript-algorithms/src/algorithms/sorting/counting-sort/CountingSort.js",
            "./benchmark/javascript-algorithms/src/data-structures/tree/red-black-tree/RedBlackTree.js"
            ],
        "./benchmark/lodash": [
            "./benchmark/lodash/.internal/equalArrays.js",
            "./benchmark/lodash/hasPath.js",
            "./benchmark/lodash/random.js",
            "./benchmark/lodash/result.js",
            "./benchmark/lodash/slice.js",
            "./benchmark/lodash/split.js",
            "./benchmark/lodash/toNumber.js",
            "./benchmark/lodash/transform.js",
            "./benchmark/lodash/truncate.js",
            "./benchmark/lodash/unzip.js"
            ]
        # "./benchmark/moment": [
        #     "./benchmark/moment/src/lib/moment/add-subtract.js",
        #     "./benchmark/moment/src/lib/moment/calendar.js",
        #     "./benchmark/moment/src/lib/create/check-overflow.js",
        #     "./benchmark/moment/src/lib/moment/compare.js",
        #     "./benchmark/moment/src/lib/moment/constructor.js",
        #     "./benchmark/moment/src/lib/create/date-from-array.js",
        #     "./benchmark/moment/src/lib/moment/format.js",
        #     "./benchmark/moment/src/lib/create/from-anything.js",
        #     "./benchmark/moment/src/lib/create/from-array.js",
        #     "./benchmark/moment/src/lib/create/from-object.js",
        #     "./benchmark/moment/src/lib/create/from-string-and-array.js",
        #     "./benchmark/moment/src/lib/create/from-string-and-format.js",
        #     "./benchmark/moment/src/lib/create/from-string.js",
        #     "./benchmark/moment/src/lib/moment/get-set.js",
        #     "./benchmark/moment/src/lib/create/locale.js",
        #     "./benchmark/moment/src/lib/moment/min-max.js",
        #     "./benchmark/moment/src/lib/moment/now.js",
        #     "./benchmark/moment/src/lib/create/parsing-flags.js",
        #     "./benchmark/moment/src/lib/moment/start-end-of.js",
        #     "./benchmark/moment/src/lib/create/valid.js"
        #     ]
    }
    index = 1
    for iteration in range(iterations):
        for preset in range(presets):
            for project, files in projects.items():
                for filepath in files:
                    if index_to_look_for == index:
                        return f'{filepath}'
                    index = index + 1

if __name__ == '__main__':
    main(sys.argv[1])