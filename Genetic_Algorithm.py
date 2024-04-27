import random
import math


class Genetic_Algorithm:
    def __init__(
        self,
        max_value,
        min_value,
        generations,
        population_size,
        mutation_rate,
        code_length=10,
    ):
        self.max_value = max_value
        self.min_value = min_value
        self.generations = generations
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        if (
            self.get_decimal_places(max_value) >= 10
            or self.get_decimal_places(min_value) >= 10
        ):
            self.code_length = max(
                self.get_decimal_places(max_value), self.get_decimal_places(min_value)
            )
        else:
            self.code_length = code_length

    # 获取小数点后的位数以决定二进制编码的长度
    def get_decimal_places(self, number):
        s = str(number)
        if "." in s:
            return len(s.split(".")[1])
        else:
            return 0

    # 定义适应度函数
    def fitness_function(self, x):
        # return math.exp(-(x - 0.1)**2) * math.sin(5 * math.pi * (x**(3/4)))**6
        # return x * math.sin(10 * math.pi * x) + 1.0
        return math.sin(x)

    # 生成二进制编码
    def generate_random_binary(self, code_length):
        if code_length <= 0:
            raise ValueError("Length must be a positive integer")
        else:
            num = bin(random.getrandbits(code_length))[2:]
            if len(num) < code_length:
                return "0" * (code_length - len(num)) + num
            return num

    # 使用二进制初始化种群
    def initialize_population(self):
        population = []
        for _ in range(self.population_size):
            individual = self.generate_random_binary(self.code_length)
            population.append(individual)
        return population

    # 解码函数
    def decode(self, individual):
        sum_ = 0
        for i in range(len(individual)):
            sum_ += int(individual[i]) * (2**i)
        return (
            self.min_value
            + (self.max_value - self.min_value) / (2 ** len(individual) - 1) * sum_
        )

    # 选择操作：轮盘赌选择
    def roulette_wheel_selection(self, population, fitness_values):
        total_fitness = sum(fitness_values)
        selection_probabilities = [
            fitness / total_fitness for fitness in fitness_values
        ]
        selected_index = random.choices(
            range(len(population)), weights=selection_probabilities
        )[
            0
        ]  # 类似R语言的table函数
        return population[selected_index]

    # 交叉操作：单点交叉
    def crossover(self, parent1, parent2):
        crossover_point = random.randint(0, len(parent1) - 1)
        child1 = parent1[0:crossover_point] + parent2[crossover_point:]
        child2 = parent2[0:crossover_point] + parent1[crossover_point:]
        return child1, child2

    # 变异操作：简单的随机变异
    def mutation(self, individual):
        if random.random() < self.mutation_rate:
            mutated_gene_point = random.randint(0, len(individual) - 1)
            if individual[mutated_gene_point] == "0":
                individual = list(individual)
                individual[mutated_gene_point] = "1"
                individual = "".join(individual)
            else:
                individual = list(individual)
                individual[mutated_gene_point] = "0"
                individual = "".join(individual)
            return max(
                [
                    "0" * self.code_length,
                    min(
                        [individual, "1" * self.code_length],
                        key=lambda x: self.decode(x),
                    ),
                ],
                key=lambda x: self.decode(x),
            )
        return individual

    # 遗传算法主函数
    def genetic_algorithm(self):
        population = self.initialize_population()
        for _ in range(self.generations):
            # 计算适应度值
            fitness_values = [
                self.fitness_function(self.decode(individual))
                for individual in population
            ]
            # 选择新一代个体
            new_population = []
            for _ in range(self.population_size // 2):  # 每次选择一半的个体
                parent1 = self.roulette_wheel_selection(population, fitness_values)
                parent2 = self.roulette_wheel_selection(population, fitness_values)
                child1, child2 = self.crossover(parent1, parent2)
                child1 = self.mutation(child1)
                child2 = self.mutation(child2)
                new_population.extend([child1, child2])
            population = new_population[: self.population_size]  # 保持种群大小一致
        # 返回最优解
        best_individual = max(
            population,
            key=lambda x: self.fitness_function(self.decode(x)),
        )
        return self.decode(best_individual), self.fitness_function(
            self.decode(best_individual)
        )
