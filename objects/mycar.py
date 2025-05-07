class mycar:
    def __init__(self, brand, model, tream, color, seats, wheels, reams):
        
        self.brand = brand
        self.model = model
        self.tream = tream
        self.color = color
        self.seats = seats
        self.wheels = wheels
        self.reams = reams

car = mycar("Porsche", "Cayenne", "Turbo s", "grey", "leather black & red", "4 X 4", "alloy reams")

print(car.color, car.brand, car.model, car.tream)