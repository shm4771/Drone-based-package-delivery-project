#distance = 6000 # m
#payload = 5 # kg
V = 14.8 # taken 4 cell Lipo battery
battery_cr_dis = 0.80 # 80 percentage
rate = 5 # charging price for per kwh
speed = 7 # m/s
frame_weight = 1 # kg
TTWR = 1.5 # thrust to weight ratio
g = 9.8 # m/s^2


def AmpRate(payload, distance):
    battery_weight = 0.5 # kg
    TOF = distance / speed # time of flight
    Power = TTWR * (battery_weight + frame_weight + payload) * speed * g
    Amp_rating = (Power * TOF * 1000) / (V * battery_cr_dis * 3600) #mAh ( 1000/36000) factor

    max_iter = 100
    start_iter = 0

    while (start_iter < max_iter):
        start_iter += 1
        Power = TTWR * (battery_weight + frame_weight + payload) * speed * g
        Amp_rating = (Power * TOF * 1000) / (V * battery_cr_dis * 3600) #mAh ( 1000/36000) factor
        battery_weight = 0.0005 * (Amp_rating**0.8182)

    Total_Energy = (Power * TOF) / 3600000 # kWh
    Total_cost = Total_Energy * rate #Total charging cost of electricity
    #print(Total_cost)
    #print(battery_weight)
    #print("local ", Amp_rating)
    return Amp_rating


def BatWeight(Amp_rating):
    battery_weight = 0.0005 * (Amp_rating**0.8182)
    return battery_weight

def Cost(Amp_rating, weight, payload, distance):
    Total_Energy = (Amp_rating * V) / (10**6)  # kwHr
    Cost  = 2 + 3 *(Total_Energy * rate)
    return Cost



def main():
    print("Nothing")

if __name__ == '__main__':
    main()