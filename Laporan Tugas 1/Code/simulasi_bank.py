import simpy
import random
import statistics


random.seed(42)

# Parameter simulasi
NUM_TELLERS = 4  
ARRIVAL_RATES = [3, 12, 24]  
SERVICE_TIME_MEAN = 15  
SIMULATION_TIME = 480  

def customer(env, name, tellers, waiting_times, service_times):
    """ Simulasi nasabah yang datang ke bank. """
    arrival_time = env.now
    print(f"Nasabah {name} tiba pada {arrival_time:.2f} menit.")

    with tellers.request() as request:
        yield request  # Menunggu layanan
        wait_time = env.now - arrival_time
        waiting_times.append(wait_time)  # Catat waktu tunggu
        print(f"Nasabah {name} mulai dilayani setelah menunggu {wait_time:.2f} menit.")

        service_time = random.expovariate(1 / SERVICE_TIME_MEAN)
        service_times.append(service_time)  
        yield env.timeout(service_time)

        print(f"Nasabah {name} selesai dalam {service_time:.2f} menit.\n")

def customer_generator(env, tellers, arrival_rate, waiting_times, service_times):
    """ Generator nasabah yang datang ke bank. """
    customer_count = 0
    while True:
        yield env.timeout(random.expovariate(arrival_rate / 60)) 
        customer_count += 1
        env.process(customer(env, customer_count, tellers, waiting_times, service_times))

def run_simulation(arrival_rate):
    """ Menjalankan simulasi bank berdasarkan tingkat kedatangan nasabah. """
    env = simpy.Environment()
    tellers = simpy.Resource(env, capacity=NUM_TELLERS)
    waiting_times = []  
    service_times = []  

    env.process(customer_generator(env, tellers, arrival_rate, waiting_times, service_times))
    env.run(until=SIMULATION_TIME)
    
    # Hitung metrik simulasi
    avg_waiting_time = statistics.mean(waiting_times) if waiting_times else 0
    total_service_time = sum(service_times)
    utilization = (total_service_time / (NUM_TELLERS * SIMULATION_TIME)) * 100

    # Tentukan efisiensi jumlah teller
    if utilization < 50:
        employee_efficiency = "Jumlah teller Berlebihan"
    elif 50 <= utilization <= 90:
        employee_efficiency = "Jumlah teller CUKUP"
    else:
        employee_efficiency = "Jumlah teller PERLU DITAMBAH"

    print("="*40)
    print(f"Tingkat Kedatangan   : {arrival_rate} nasabah/jam")
    print(f"Rata-rata Waktu Tunggu : {avg_waiting_time:.2f} menit")
    print(f"Utilisasi Sistem      : {utilization:.2f}%")
    print(f"Efisiensi Teller      : {employee_efficiency}")
    print("="*40 + "\n")

# Jalankan simulasi untuk tingkat kedatangan yang berbeda
for rate in ARRIVAL_RATES:
    run_simulation(rate)
