import matplotlib.pyplot as plt

def show_sales_chart(sales_data):
    labels = [row[1] for row in sales_data]
    values = [row[-1] for row in sales_data]

    plt.bar(labels, values)
    plt.title("Sales by Customer")
    plt.xlabel("Customer")
    plt.ylabel("Amount")
    plt.show()
