#include <inery/inery.hpp>
#include <string>
#include <vector>

using namespace inery;
using std::string;
using std::vector;

CONTRACT orbiter : public contract
{
    static uint64_t hash_name(const string &name)
    {
        return std::hash<string>{}(name);
    }

public:
    using contract::contract;

    TABLE sidechain
    {
        string chain_name;
        string description;

        uint64_t primary_key() const { return hash_name(chain_name); }
    };

    typedef multi_index<"sidechains"_n, sidechain> sidechain_table;

    TABLE nodeurl
    {
        string rpc_url;
        string chain_name;

        uint64_t primary_key() const { return hash_name(rpc_url); }
        uint64_t by_name() const { return hash_name(chain_name); }
    };

    typedef multi_index<"nodeurls"_n, nodeurl,
                        indexed_by<"byname"_n, const_mem_fun<nodeurl, uint64_t, &nodeurl::by_name>>>
        nodeurl_table;

    TABLE database
    {
        name db_name;
        string chain_name;

        uint64_t primary_key() const { return db_name.value; }
        uint64_t by_sidechain() const { return hash_name(chain_name); }
    };
    typedef multi_index<"databases"_n, database,
                        indexed_by<"bysidechain"_n, const_mem_fun<database, uint64_t, &database::by_sidechain>>>
        database_table;

    ACTION hsh(string name)
    {
        print(hash_name(name));
    }
    ACTION adddatabase(name db_name, string chain_name)
    {
        require_auth(get_self());

        database_table db_table(get_self(), get_self().value);

        auto chainname_hash = hash_name(chain_name);

        auto existing = db_table.find(db_name.value);
        check(existing == db_table.end(), ("Database with this name already registered on sidechain " + existing->chain_name).c_str());

        db_table.emplace(get_self(), [&](auto &row)
                         {
            row.db_name = db_name;
            row.chain_name = chain_name; });
    }

    // Akcija za registraciju sidechain-a
    ACTION regsidechain(string chain_name, string rpc_url, string description)
    {
        require_auth(get_self());

        auto url_hash = hash_name(rpc_url);
        auto name_hash = hash_name(chain_name);

        sidechain_table _sidechains(get_self(), get_self().value);
        auto existing = _sidechains.find(name_hash);
        check(existing == _sidechains.end(), "Sidechain with this name already exists.");

        _sidechains.emplace(get_self(), [&](auto &row)
                            {
            row.chain_name = chain_name;
            row.description = description; });

        nodeurl_table _nodetbl(get_self(), get_self().value);
        auto existing2 = _nodetbl.find(url_hash);
        check(existing2 == _nodetbl.end(), "Side Chain URL is already registered");

        _nodetbl.emplace(get_self(), [&](auto &row)
                         {
            row.rpc_url = rpc_url;
            row.chain_name = chain_name; });
    }

    // (Opcionalno) Akcija za brisanje sidechain-a
    ACTION remsidechain(string chain_name)
    {
        require_auth(get_self());

        // 1. Brisanje iz tabele sidechains
        sidechain_table _sidechains(get_self(), get_self().value);
        auto itr = _sidechains.find(hash_name(chain_name));
        check(itr != _sidechains.end(), "Sidechain not found.");
        _sidechains.erase(itr);

        // 2. Brisanje iz tabele nodeurl
        nodeurl_table _nodetbl(get_self(), get_self().value);
        auto name_index = _nodetbl.get_index<"byname"_n>();

        auto name_hash = hash_name(chain_name);
        auto itr2 = name_index.lower_bound(name_hash);

        // Moraš koristiti next() nakon brisanja, jer erase invalidira iterator
        while (itr2 != name_index.end() && itr2->chain_name == chain_name)
        {
            itr2 = name_index.erase(itr2); // Pravilno brisanje i dobijanje sledećeg iteratora
        }
    }
};
