#include <inery/inery.hpp>
using namespace inery;

CONTRACT database : public contract
{
public:
    using contract::contract;

    // Struktura zapisa
    TABLE record
    {
        uint64_t id;
        name user;
        std::string data;

        uint64_t primary_key() const { return id; }
    };

    typedef multi_index<"records"_n, record> record_table;

    // Dodavanje novog zapisa
    ACTION addrecord(name user, uint64_t id, std::string data)
    {
        require_auth(user);

        record_table records(get_self(), get_self().value);
        auto itr = records.find(id);
        check(itr == records.end(), "Record with this ID already exists.");

        records.emplace(user, [&](auto &row)
                        {
            row.id = id;
            row.user = user;
            row.data = data; });
    }

    // Ažuriranje postojećeg zapisa
    ACTION updaterecord(name user, uint64_t id, std::string new_data)
    {
        require_auth(user);

        record_table records(get_self(), get_self().value);
        auto itr = records.find(id);
        check(itr != records.end(), "Record not found.");
        check(itr->user == user, "Only the owner can update the record.");

        records.modify(itr, user, [&](auto &row)
                       { row.data = new_data; });
    }

    // Brisanje zapisa
    ACTION deleterecord(name user, uint64_t id)
    {
        require_auth(user);

        record_table records(get_self(), get_self().value);
        auto itr = records.find(id);
        check(itr != records.end(), "Record not found.");
        check(itr->user == user, "Only the owner can delete the record.");

        records.erase(itr);
    }
};
