import streamlit as st
import math_model


def main():
    st.title('Wood plank transportation')
    st.sidebar.header("Navigation")
    option = st.sidebar.radio(' ', ('Application', 'Documentation'))

    if option == "Application":
        uploaded_file = st.file_uploader("Get input file (.xlsx)", type="xlsx", encoding=None)
        if uploaded_file is not None:
            factories, warehouses, customers, distance = math_model.read_data(uploaded_file)
            is_optimize = st.button("Optimize")
            if is_optimize:
                x, y = math_model.solve(factories, warehouses, customers, distance)
                st.header('Layout')
                st.write(math_model.plot(factories, warehouses, customers, x, y))

    if option == "Documentation":
        fo = open("math_model.md", "r")
        st.write(fo.read())


if __name__ == "__main__":
    main()