#pragma once

#include <godot_cpp/classes/node.hpp>
#include <godot_cpp/variant/string.hpp>

namespace godot
{
    class MyNode : public Node
    {
        GDCLASS(MyNode, Node)

    public:
        MyNode() = default;
        ~MyNode() = default;

        void _ready() override;
        void _process(double delta) override;

        void set_speed(double speed);
        double get_speed() const;

    protected:
        static void _bind_methods();

    private:
        double m_Speed = 1.0;
        double m_TimeElapsed = 0.0;
    };
}
