#include <map>
#include <string>

// g++ -std=c++11 -shared -fPIC -Wl,-soname,ex_map.so.1 -o ex_map.so ex_map.c

extern "C" {

    std::map<std::string, int> * ex_map_alloc(  ) {
        return new std::map<std::string, int>();
    }

    void ex_map_free( std::map<std::string, int> * map_ptr ) {
        delete(map_ptr);
    }

    int ex_map_size( std::map<std::string, int> * map_ptr ) {
        return map_ptr->size();
    }

    void ex_map_insert( std::map<std::string, int> * map_ptr, char* key, int val ) {
        map_ptr->emplace(key, val);
    }

    const char* ex_map_get_key_at( std::map<std::string, int> * map_ptr, int it ) {
        return std::next( map_ptr->begin(), it )->first.data();
    }

    int ex_map_find( std::map<std::string, int> * map_ptr, char* key ) {
        auto ret = map_ptr->find(key);
        if (ret != map_ptr->end()) {
                return ret->second;
        }
        return 42;
    }

    int ex_map_count(std::map<std::string, int> * map_ptr, char* key ) {
        return map_ptr->count(key);
    }
}

template class std::map<std::string, int>;
