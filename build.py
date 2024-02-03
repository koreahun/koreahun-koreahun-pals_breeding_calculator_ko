import pandas as pd
import streamlit as st
import chardet
import pandas as pd

def detect_encoding(file_path):
    # 파일을 바이너리 모드로 열어서 인코딩 감지
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']

# 파일의 인코딩 감지
file_encoding = detect_encoding(r'Data/Images.csv')

# 디코딩 에러를 방지하기 위해 인코딩 감지를 통해 얻은 인코딩으로 파일 읽기 시도
try:
    sources = pd.read_csv(r'Data/Images.csv', sep=',', header=None, encoding=file_encoding)
except UnicodeDecodeError:
    print(f"UTF-8로 디코딩하는 데 문제가 있어서 {file_encoding}으로 다시 시도합니다.")

    # 인코딩 감지를 통해 얻은 인코딩으로 파일을 열지 못하는 경우 대안으로 'utf-16' 사용
    try:
        sources = pd.read_csv(r'Data/Images.csv', sep=',', header=None, encoding='utf-16')
        print(f"{file_encoding}로 디코딩하는 데 성공했습니다.")
    except UnicodeDecodeError:
        print("UTF-16로도 디코딩하는 데 문제가 있습니다. 다른 인코딩을 시도해 보세요.")

# 웹페이지 설정
st.set_page_config(layout="wide")

# ---------------------------- 데이터 로딩 ------------------------------- #
@st.cache_data
def load_pals():
    pals = pd.read_csv(r'Data/Pals.csv', header=None, encoding='utf-8')
    number_of_pals = len(pals[0])
    return pals, number_of_pals

@st.cache_data
def load_all_combinations():
    all_combos = pd.read_csv(r'Data/AllCombos.csv', sep=';', header=None, encoding='utf-8')
    return all_combos

@st.cache_data
def load_images_src():
    sources = pd.read_csv(r'Data/Images.csv', sep=',', header=None, encoding='utf-8')
    return sources

@st.cache_data
def load_wikis_url():
    sources = pd.read_csv(r'Data/Wikis.csv', sep=',', header=None, encoding='utf-8')
    return sources

# 데이터 로딩
df_pals, n_pals = load_pals()
df_all_combos = load_all_combinations()
img_sources = load_images_src()
wikis_url = load_wikis_url()

# ---------------------------- 데이터 함수 ------------------------- #

def search_number(pal):
    number = df_pals[df_pals[0] == pal].index[0]
    return number


def search_pal(number):
    pal = df_pals[0][number]
    return pal


def get_pals_list():
    pals = []
    for pal in df_pals[0]:
        pals.append(pal)
    return pals


def get_children(parent1, parent2):
    column = search_number(parent1)
    row = search_number(parent2)
    children = df_all_combos[column][row]
    return children


def get_combinations(pal):
    combinations = []
    for column in range(n_pals):
        for row, p in enumerate(df_all_combos[column].values):
            if p == pal:
                parent1 = search_pal(column)
                parent2 = search_pal(row)
                parents = [parent1, parent2]
                if not [parent2, parent1] in combinations:
                    combinations.append(parents)
    return combinations


def get_image(pal):
    if pal in img_sources[0].values:
        row = img_sources[img_sources[0] == pal].index[0]
        image_src = img_sources[1][row]
        return image_src
    else:
        row = img_sources[img_sources[0] == "No Image"].index[0]
        no_image_src = img_sources[1][row]
        return no_image_src


def get_wiki(pal):
    if pal in wikis_url[0].values:
        row = wikis_url[wikis_url[0] == pal].index[0]
        url = wikis_url[1][row]
        return url
    else:
        return False

def image_with_wiki(pal, place=st):
    href = get_wiki(pal)
    src = get_image(pal)
    place.markdown(f'''
        <a href="{href}">
            <img src="{src}" />
        </a>''', unsafe_allow_html=True)


# ---------------------------- 웹 앱 빌드 -------------------------- #

# 헤더
with st.container():
    c1, c2, c3 = st.columns(3)
    c1.text("게임 버전: 0.1.3.0")
    c1.write("[https://github.com/beckerfelipee](https://github.com/beckerfelipee)")
    c1.link_button("커피 살게요!", "https://www.buymeacoffee.com/beckerfelipee")
    c2.title('팰월드 교배 :blue[계산기]', anchor=False)

# Calculator Area

with st.container():
    st.divider()
    left, space1, center1, space2, center2, space3, center3, space4, right = st.columns([3, 1, 2, 1, 2, 1, 2, 1, 3])
    pals_list = get_pals_list()

    # Tips
    if left.button('Some tips!'):
        st.toast('You can click on "Search for Pal" to view all combinations for breeding a pal.', icon='👀')
        st.toast('You can click on the pal image to open their wiki.', icon='🚀')
        st.toast('Switch light and dark themes by clicking Settings in the top right corner.', icon='🌃')

    # Parent 1
    center1.header("Parent 1", anchor=False)
    pal1 = center1.selectbox("pal1", pals_list, label_visibility="hidden")
    image_with_wiki(pal1, center1)

    # Parent 2
    center2.header("Parent 2", anchor=False)
    pal2 = center2.selectbox("pal2", pals_list, label_visibility="hidden")
    image_with_wiki(pal2, center2)

    # Result
    center3.header("Result", anchor=False)
    center3.markdown("")
    pal3 = get_children(pal1, pal2)
    center3.code(pal3)
    image_with_wiki(pal3, center3)
    st.divider()

    # Some Easter Egg (Subscribe to Gaubss)
    if pal1 == "Bushi" and pal2 == "Penking":
        st.toast('Subscribe to Gaubss Youtube Channel!', icon='🔺')

# Search by Result
with st.expander("Search for Pal"):
    st.divider()
    st.header("Search for Pal", anchor=False)
    l, s1, r1, s2, r2, s3, r3, s4, r4 = st.columns([3, 1, 3, 1, 3, 1, 3, 1, 3])

    # Pal for Search
    pal4 = l.selectbox("pal4", pals_list, label_visibility="hidden")

    # get combinations
    result = get_combinations(pal4)

    # Create Filter
    possible_pals = []
    for c in result:
        if not c[0] in possible_pals:
            possible_pals.append(c[0])
        if not c[1] in possible_pals:
            possible_pals.append(c[1])

    filter_option = l.selectbox("Filter by parent", possible_pals, index=None)

    # Pal Image
    image_with_wiki(pal4, l)
    l.divider()

    with st.container():
        # Return combinations
        r_list = [r1, r2, r3, r4]
        index = 0
        for c in result:
            if filter_option:
                if filter_option in c:
                    couple = f"{c[0]} + {c[1]}"
                    r_list[index].code(couple)
                    index = (index + 1) % len(r_list)
            else:
                couple = f"{c[0]} + {c[1]}"
                r_list[index].code(couple)
                index = (index + 1) % len(r_list)
