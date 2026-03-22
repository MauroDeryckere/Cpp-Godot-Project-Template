#pragma once

#include <godot_cpp/classes/node.hpp>

namespace godot
{
    class MyNode : public Node
    {
        GDCLASS(MyNode, Node)

    public:
        MyNode() = default;
        ~MyNode() = default;

        void _process(double delta);

    protected:
        static void _bind_methods();
    };
}