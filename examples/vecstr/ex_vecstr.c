#include <algorithm> // std::find
#include <vector>
#include <string>
#include <iterator>

// g++ -std=c++11 -shared -fPIC -Wl,-soname,ex_vecstr.so.1 -o ex_vecstr.so ex_vecstr.c

extern "C" {

    std::vector<std::string> * ex_vecstr_alloc(  ) {
        return new std::vector<std::string>();
    }

    void ex_vecstr_free( std::vector<std::string> * vec_ptr ) {
        delete(vec_ptr);
    }

    int ex_vecstr_size( std::vector<std::string> * vec_ptr ) {
        return vec_ptr->size();
    }

    void ex_vecstr_push_back( std::vector<std::string> * vec_ptr, const char* elt ) {
        vec_ptr->push_back(elt);
    }

    void ex_vecstr_insert( std::vector<std::string> * vec_ptr, const char* elt, int index ) {
        vec_ptr->at(index) = elt;
    }

    const char* ex_vecstr_at( std::vector<std::string> * vec_ptr, int index ) {
        return vec_ptr->at(index).data();
    }

    int ex_vecstr_find( std::vector<std::string> * vec_ptr, char* key ) {
        std::vector<std::string>::iterator ret = std::find(vec_ptr->begin(), vec_ptr->end(), key);
        if (ret != vec_ptr->end()) {
            return std::distance(vec_ptr->begin(), ret);
        }
        return -1;
    }
}

template class std::vector<std::string>;
