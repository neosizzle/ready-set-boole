
#include <benchmark/benchmark.h>

#include <algorithm>
#include <numeric>
#include <string>
#include <vector>

// Generate input data
static std::vector<int> GenerateData(int n) {
    std::vector<int> data(n);
    std::iota(data.begin(), data.end(), 1);
    return data;
}

// O(1) - Constant Time
static void BM_Constant(benchmark::State& state) {
    auto data = GenerateData(state.range(0));

    for (auto _ : state) {
        benchmark::DoNotOptimize(data[data.size() / 2]);
    }
}

// O(log n) - Binary Search
static void BM_BinarySearch(benchmark::State& state) {
    auto data = GenerateData(state.range(0));

    for (auto _ : state) {
        auto result = std::binary_search(
            data.begin(), data.end(), data.back()
        );
        benchmark::DoNotOptimize(result);
    }
}

// O(n) - Linear Search
static void BM_LinearSearch(benchmark::State& state) {
    auto data = GenerateData(state.range(0));

    for (auto _ : state) {
        auto result = std::find(
            data.begin(), data.end(), data.back()
        );
        benchmark::DoNotOptimize(result);
    }
}

// O(n log n) - Sorting
static void BM_MergeSort(benchmark::State& state) {
    auto original = GenerateData(state.range(0));

    for (auto _ : state) {
        auto data = original;

        std::stable_sort(data.begin(), data.end());

        benchmark::DoNotOptimize(data);
    }
}

// O(n^2) - Bubble Sort
static void BM_BubbleSort(benchmark::State& state) {
    auto original = GenerateData(state.range(0));

    for (auto _ : state) {
        auto data = original;

        for (size_t i = 0; i < data.size(); i++) {
            for (size_t j = 0; j + 1 < data.size() - i; j++) {
                if (data[j] > data[j + 1]) {
                    std::swap(data[j], data[j + 1]);
                }
            }
        }

        benchmark::DoNotOptimize(data);
    }
}

// Register benchmarks

BENCHMARK(BM_Constant)
    ->RangeMultiplier(2)
    ->Range(128, 8192)
    ->Complexity(benchmark::o1);

BENCHMARK(BM_BinarySearch)
    ->RangeMultiplier(2)
    ->Range(128, 8192)
    ->Complexity(benchmark::oLogN);

BENCHMARK(BM_LinearSearch)
    ->RangeMultiplier(2)
    ->Range(128, 8192)
    ->Complexity(benchmark::oN);

BENCHMARK(BM_MergeSort)
    ->RangeMultiplier(2)
    ->Range(128, 8192)
    ->Complexity(benchmark::oNLogN);

BENCHMARK(BM_BubbleSort)
    ->RangeMultiplier(2)
    ->Range(128, 8192)
    ->Complexity(benchmark::oNSquared);

// Main
BENCHMARK_MAIN();
